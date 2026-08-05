#!/usr/bin/env python3
"""Merge job-search/seen_jobs.json and job-search/tracker.csv into job-search/pipeline.csv.

pipeline.csv is the single source of truth for the dashboard: one row per
job ever surfaced, carrying the whole lifecycle from "found by the daily search"
through to "offer" or "discarded".

The merge is non-destructive by design. A field that already has a value in
pipeline.csv is never overwritten by a sync -- the CSV is hand-edited (pros,
cons, company_url, notes) and those edits must survive the next daily scrape.
Status only ever moves forward through STATUS_RANK; a scraper entry that still
says "new" cannot pull a row back from "interviewing".

Usage:
    python tools/sync_pipeline.py            # merge and write
    python tools/sync_pipeline.py --dry-run  # report what would change

Run it from your workspace (the directory that holds `job-search/`).
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

def find_workspace(start: Path | None = None) -> Path:
    """Locate the `job-search/` state directory.

    Scripts live inside the installed skill (often ~/.claude/skills/), while the
    data lives in whatever workspace the user ran Claude from -- so resolve from
    the current directory, not from __file__.
    """
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "job-search").is_dir():
            return candidate / "job-search"
    return here / "job-search"


WS = find_workspace()

PIPELINE = WS / "pipeline.csv"
SEEN = WS / "seen_jobs.json"
TRACKER = WS / "tracker.csv"

FIELDS = [
    "id", "date_found", "date_applied", "last_update",
    "company", "company_url", "role", "role_type", "sector", "company_type",
    "fit", "status", "posting_url", "location", "modality", "comp",
    "english_req", "pros", "cons", "notes", "source",
    "cv_file", "cover_letter_file", "contact",
]

# Lifecycle vocabulary. "Open" is everything that still needs a decision.
OPEN_STATUSES = {"new", "interested", "applied", "interviewing", "offer"}
CLOSED_STATUSES = {"rejected", "discarded", "no_response", "withdrawn", "hired"}

# A sync may only move a row rightwards along this ladder.
STATUS_RANK = {
    "discarded": 0,
    "new": 1,
    "interested": 2,
    "applied": 3,
    "interviewing": 4,
    "offer": 5,
    "hired": 6,
}
# Terminal states set by a human or by /outcome; a sync never overrides them.
TERMINAL = {"rejected", "discarded", "no_response", "withdrawn", "hired"}

# job_search_tracker.csv uses its own status words; map them onto the ladder.
TRACKER_STATUS = {
    "cv_ready": "interested",
    "applied": "applied",
    "in_progress": "applied",
    "interview_scheduling": "interviewing",
    "interview_in_progress": "interviewing",
    "interview": "interviewing",
    "offer": "offer",
    "hired": "hired",
    "rejected": "rejected",
    "no_response": "no_response",
    "withdrawn_by_candidate": "withdrawn",
    "withdrawn": "withdrawn",
}

FIT_MAP = {"high": "high", "good": "medium", "medium": "medium", "low": "low", "": ""}

# seen_jobs.json accumulated free-text statuses over time ("skipped_mexico_only",
# "discarded_2026-07-28_..."). Anything not recognised collapses to discarded,
# with the original string preserved in notes so the reason is not lost.
def normalise_seen_status(raw: str) -> tuple[str, str]:
    raw = (raw or "").strip()
    if raw in STATUS_RANK or raw in TERMINAL:
        return raw, ""
    if raw.startswith("applied"):
        return "applied", ""
    if raw.startswith("closed"):
        return "no_response", raw
    if raw.startswith("evaluated"):
        return "new", raw
    if raw.startswith(("skipped", "discarded")):
        return "discarded", raw
    return "new", raw


# Past runs appended the rejection reason onto the job title in seen_jobs.json
# ("Senior PM - payments PM not AI, rejected"). Split those back apart so the
# role column stays a real job title and the reason lands in notes.
REASON_MARKERS = (
    "rejected", "deprioritized", "unverifiable", "unreadable", "duplicate",
    "hybrid", "onsite", "not ai", "heavy engineering", "talent pool",
    "commercial gm role", "posting removed", "no longer available",
)


def split_role_reason(title: str) -> tuple[str, str]:
    title = (title or "").strip()
    if " - " not in title:
        return title, ""
    head, _, tail = title.rpartition(" - ")
    if any(marker in tail.lower() for marker in REASON_MARKERS) and head.strip():
        return head.strip(), tail.strip()
    return title, ""


def slug(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60]


# Free text in modality/source makes the dashboard dropdowns unusable -- every
# hand-written variant becomes its own option. Collapse both to a fixed
# vocabulary on every write so the file is self-healing.
MODALITY_VALUES = ("remote", "hybrid", "onsite", "unverified")


def norm_modality(value: str) -> str:
    low = (value or "").strip().lower()
    if not low:
        return ""
    if "unverified" in low or "unconfirmed" in low:
        return "unverified"
    for key in ("hybrid", "hibrid", "onsite", "on-site", "presencial", "remote", "remoto"):
        if key in low:
            return {"hibrid": "hybrid", "on-site": "onsite", "presencial": "onsite",
                    "remoto": "remote"}.get(key, key)
    return "unverified"


SOURCE_ALIASES = {
    "linkedin-search": "linkedin", "linkedin-saved": "linkedin",
    "linkedin easy apply": "linkedin", "linkedin/gem": "linkedin",
    "linkedin / ashby": "linkedin", "freehire-search": "freehire",
    "freehire / linkedin": "freehire", "company careers site": "company",
    "company careers form": "company", "company careers site (oracle cx)": "company",
    "direct application": "company", "direct outreach": "outreach",
}


def norm_source(value: str) -> str:
    low = (value or "").strip().lower()
    return SOURCE_ALIASES.get(low, low)


def normalise_row(row: dict) -> dict:
    row["modality"] = norm_modality(row.get("modality", ""))
    row["source"] = norm_source(row.get("source", ""))
    return row


def make_id(company: str, role: str) -> str:
    """Dedupe key. Company+role, never URL: the same posting shows up on
    LinkedIn, Greenhouse and freehire with three different URLs."""
    return f"{slug(company)}__{slug(role)}"


def blank_row() -> dict:
    return {f: "" for f in FIELDS}


def read_pipeline() -> dict[str, dict]:
    if not PIPELINE.exists():
        return {}
    with PIPELINE.open(encoding="utf-8-sig", newline="") as fh:
        rows = {}
        for row in csv.DictReader(fh):
            merged = blank_row()
            merged.update({k: (v or "") for k, v in row.items() if k in FIELDS})
            if not merged["id"]:
                merged["id"] = make_id(merged["company"], merged["role"])
            rows[merged["id"]] = merged
        return rows


def fill(existing: dict, incoming: dict, changed: list) -> None:
    """Copy incoming values into empty fields only. Never clobber a human edit."""
    for key, value in incoming.items():
        if key in ("id", "status"):
            continue
        if value and not existing.get(key):
            existing[key] = value
            changed.append(key)


def advance_status(existing: dict, new_status: str, changed: list) -> None:
    current = existing.get("status") or "new"
    if current in TERMINAL and new_status not in TERMINAL:
        return
    if new_status in TERMINAL and current not in TERMINAL:
        existing["status"] = new_status
        changed.append("status")
        return
    if STATUS_RANK.get(new_status, -1) > STATUS_RANK.get(current, -1):
        existing["status"] = new_status
        changed.append("status")


def merge_seen(rows: dict[str, dict], report: list) -> None:
    if not SEEN.exists():
        return
    data = json.loads(SEEN.read_text(encoding="utf-8-sig")).get("seen", {})
    for url, entry in data.items():
        company = (entry.get("company") or "").strip()
        role, title_reason = split_role_reason(entry.get("title") or "")
        if not company or not role:
            continue
        status, reason = normalise_seen_status(entry.get("status", ""))
        reason = "; ".join(x for x in (title_reason, reason) if x)
        key = make_id(company, role)
        incoming = {
            "date_found": entry.get("first_seen", ""),
            "company": company,
            "role": role,
            "fit": FIT_MAP.get((entry.get("fit") or "").strip(), ""),
            "posting_url": entry.get("url") or url,
            "source": entry.get("portal", ""),
            "notes": "; ".join(x for x in (reason, entry.get("dropped_by") or "") if x),
        }
        if key not in rows:
            row = blank_row()
            row["id"] = key
            row["status"] = status
            fill(row, incoming, [])
            rows[key] = row
            report.append(("added", key, status))
        else:
            changed: list = []
            fill(rows[key], incoming, changed)
            advance_status(rows[key], status, changed)
            if changed:
                report.append(("updated", key, ",".join(sorted(set(changed)))))


def merge_tracker(rows: dict[str, dict], report: list) -> None:
    if not TRACKER.exists():
        return
    with TRACKER.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            company = (row.get("company") or "").strip()
            role = (row.get("role") or "").strip()
            if not company or not role:
                continue
            key = make_id(company, role)
            status = TRACKER_STATUS.get((row.get("status") or "").strip(), "applied")
            incoming = {
                "date_applied": (row.get("date") or "").strip(),
                "company": company,
                "role": role,
                "role_type": (row.get("role_family") or "").strip(),
                "fit": FIT_MAP.get((row.get("fit") or "").strip(), ""),
                "notes": (row.get("notes") or "").strip(),
                "contact": (row.get("contact") or "").strip(),
                "source": (row.get("channel") or "").strip(),
            }
            if key not in rows:
                new_row = blank_row()
                new_row["id"] = key
                new_row["status"] = status
                new_row["date_found"] = incoming["date_applied"]
                fill(new_row, incoming, [])
                rows[key] = new_row
                report.append(("added", key, status))
            else:
                changed: list = []
                fill(rows[key], incoming, changed)
                advance_status(rows[key], status, changed)
                if changed:
                    report.append(("updated", key, ",".join(sorted(set(changed)))))


def write_pipeline(rows: dict[str, dict], touched: set[str]) -> None:
    """`touched` holds the ids this sync actually changed. Only those get today's
    date -- otherwise every run would restamp all 682 rows and last_update would
    say nothing about when a job really moved."""
    today = date.today().isoformat()
    ordered = sorted(
        rows.values(),
        key=lambda r: (r.get("date_found") or "", r.get("company") or ""),
        reverse=True,
    )
    for row in ordered:
        if row["id"] in touched:
            row["last_update"] = today
        elif not row.get("last_update"):
            # Backfilled row with no history: the best evidence of its last real
            # movement is when it was applied to, else when it was found.
            row["last_update"] = row.get("date_applied") or row.get("date_found") or today
        if not row.get("id"):
            row["id"] = make_id(row.get("company", ""), row.get("role", ""))
        normalise_row(row)
    PIPELINE.parent.mkdir(parents=True, exist_ok=True)
    with PIPELINE.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in ordered:
            writer.writerow({f: row.get(f, "") for f in FIELDS})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = read_pipeline()
    before = len(rows)
    report: list = []
    merge_seen(rows, report)
    merge_tracker(rows, report)

    added = [r for r in report if r[0] == "added"]
    updated = [r for r in report if r[0] == "updated"]
    touched = {r[1] for r in report}

    if args.dry_run:
        for kind, key, detail in report[:40]:
            print(f"{kind:8} {key:55} {detail}")
        if len(report) > 40:
            print(f"... and {len(report) - 40} more")
    else:
        write_pipeline(rows, touched)

    open_count = sum(1 for r in rows.values() if r.get("status") in OPEN_STATUSES)
    print(
        f"pipeline: {before} -> {len(rows)} rows "
        f"({len(added)} added, {len(updated)} updated, {open_count} open)"
    )
    if not args.dry_run:
        print(f"written: {PIPELINE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
