#!/usr/bin/env python3
"""Build a self-contained HTML dashboard from job-search/pipeline.csv.

One file, no server, no CDN, no dependencies -- open it straight from disk.
All filtering, sorting and search happen client-side over data embedded in the
page, so it keeps working offline and from a file:// URL.

Usage:
    python tools/build_dashboard.py                  # -> job-search/dashboard.html
    python tools/build_dashboard.py path/to/out.html
    python tools/build_dashboard.py --template       # empty shell, no rows

Run it from your workspace (the directory that holds `job-search/`).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
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
DEFAULT_OUT = WS / "dashboard.html"

OPEN_STATUSES = ["new", "interested", "applied", "interviewing", "offer"]

STATUS_META = {
    "new":          {"label": "Nuevo",        "color": "#3b82f6"},
    "interested":   {"label": "Interesa",     "color": "#06b6d4"},
    "applied":      {"label": "Aplicado",     "color": "#8b5cf6"},
    "interviewing": {"label": "Avanzado",     "color": "#f59e0b"},
    "offer":        {"label": "Oferta",       "color": "#22c55e"},
    "hired":        {"label": "Contratado",   "color": "#16a34a"},
    "rejected":     {"label": "Rechazado",    "color": "#ef4444"},
    "discarded":    {"label": "Descartado",   "color": "#64748b"},
    "no_response":  {"label": "Sin respuesta","color": "#94a3b8"},
    "withdrawn":    {"label": "Retirado",     "color": "#a16207"},
}

FIT_META = {
    "high":   {"label": "Alto",  "color": "#22c55e"},
    "medium": {"label": "Medio", "color": "#f59e0b"},
    "low":    {"label": "Bajo",  "color": "#94a3b8"},
    "":       {"label": "-",     "color": "#cbd5e1"},
}


# company_type is deliberately descriptive in the CSV ("early startup (NYC, seed)")
# because the employer-relationship note matters when deciding to apply. That
# makes it useless as a dropdown, so filtering runs on a coarse derived bucket
# while the table still shows the full text.
BUCKETS = [
    ("staffing", ("staffing", "recruiting intermediary", "intermediary", "aggregator")),
    ("consultancy", ("consultancy", "consulting", "it services", "delivery centre")),
    ("agency", ("agency",)),
    ("enterprise", ("enterprise", "pe-owned", "public", "holding", "corporate")),
    ("scale-up", ("scale-up", "scaleup", "scale up")),
    ("startup", ("startup", "seed", "early-stage", "early stage")),
    ("platform", ("platform", "marketplace", "gig")),
]


def company_bucket(text: str) -> str:
    low = (text or "").lower()
    if not low:
        return ""
    for name, keys in BUCKETS:
        if any(k in low for k in keys):
            return name
    return "otro"


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        rows = [{k: (v or "").strip() for k, v in row.items() if k} for row in csv.DictReader(fh)]
    for row in rows:
        row["_bucket"] = company_bucket(row.get("company_type", ""))
    return rows


def embed(payload) -> str:
    """JSON for a <script> block. Escaping </ stops a value containing a
    literal </script> from closing the tag and injecting markup."""
    return json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")


CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#f6f7f9; --panel:#fff; --ink:#0f172a; --muted:#64748b; --line:#e2e8f0;
  --accent:#4f46e5; --chip:#f1f5f9; --shadow:0 1px 2px rgba(15,23,42,.06),0 4px 16px rgba(15,23,42,.05);
}
@media (prefers-color-scheme:dark){
  :root{--bg:#0b1120;--panel:#111827;--ink:#e5e7eb;--muted:#94a3b8;--line:#1f2937;
        --accent:#818cf8;--chip:#1f2937;--shadow:0 1px 2px rgba(0,0,0,.4),0 4px 16px rgba(0,0,0,.3)}
}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
     -webkit-font-smoothing:antialiased}
.wrap{max-width:1500px;margin:0 auto;padding:20px 18px 64px}
header{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;margin-bottom:16px}
h1{font-size:20px;margin:0;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:12px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(126px,1fr));gap:10px;margin-bottom:16px}
.card{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--c,var(--accent));
      border-radius:10px;padding:11px 13px;box-shadow:var(--shadow);cursor:pointer;text-align:left;
      font:inherit;color:inherit}
.card:hover{border-color:var(--accent)}
.card[aria-pressed="true"]{outline:2px solid var(--accent);outline-offset:1px}
.card .n{font-size:24px;font-weight:700;line-height:1.15;font-variant-numeric:tabular-nums}
.card .l{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow)}
.filters{padding:12px;display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin-bottom:14px}
.filters label{display:flex;flex-direction:column;gap:3px;font-size:10px;color:var(--muted);
               text-transform:uppercase;letter-spacing:.05em}
select,input[type=search],input[type=date]{background:var(--bg);color:var(--ink);border:1px solid var(--line);
  border-radius:7px;padding:6px 9px;font:13px system-ui,sans-serif;min-height:32px}
input[type=search]{min-width:230px}
select:focus,input:focus{outline:2px solid var(--accent);outline-offset:-1px}
.spacer{flex:1 1 auto}
fieldset.statusbox{border:1px solid var(--line);border-radius:9px;margin:0;padding:7px 11px 9px;
                   display:flex;flex-wrap:wrap;align-items:center;gap:8px}
fieldset.statusbox legend{font-size:10px;color:var(--muted);text-transform:uppercase;
                          letter-spacing:.05em;padding:0 5px}
.chk{display:inline-flex;align-items:center;gap:5px;background:var(--chip);border-radius:999px;
     padding:4px 10px 4px 7px;font-size:12px;cursor:pointer;user-select:none;border:1px solid transparent}
.chk:hover{border-color:var(--accent)}
.chk input{accent-color:var(--accent);margin:0;width:13px;height:13px;cursor:pointer}
.chk .dot{width:8px;height:8px;border-radius:50%;flex:none}
.chk b{color:var(--muted);font-weight:600;font-variant-numeric:tabular-nums}
.chk:has(input:checked){background:color-mix(in srgb,var(--accent) 14%,var(--chip))}
.presets{display:flex;gap:4px}
.presets button{background:transparent;color:var(--muted);border:1px solid var(--line);
                border-radius:999px;padding:4px 10px;font:11px system-ui,sans-serif;cursor:pointer}
.presets button:hover{color:var(--ink);border-color:var(--accent)}
.btn{background:var(--chip);color:var(--ink);border:1px solid var(--line);border-radius:7px;
     padding:7px 11px;font:12px system-ui,sans-serif;cursor:pointer}
.btn:hover{border-color:var(--accent)}
.count{font-size:12px;color:var(--muted);padding:0 4px}
.tablewrap{overflow-x:auto;border-radius:12px}
table{border-collapse:collapse;width:100%;min-width:1080px;background:var(--panel)}
th,td{text-align:left;padding:9px 11px;border-bottom:1px solid var(--line);vertical-align:top}
th{position:sticky;top:0;background:var(--panel);z-index:2;font-size:11px;text-transform:uppercase;
   letter-spacing:.05em;color:var(--muted);cursor:pointer;white-space:nowrap;user-select:none}
th:hover{color:var(--ink)}
th .arrow{opacity:.4;font-size:9px}
tbody tr.row{cursor:pointer}
tbody tr.row:hover{background:color-mix(in srgb,var(--accent) 7%,transparent)}
tbody tr.row.open{background:color-mix(in srgb,var(--accent) 10%,transparent)}
td.co{font-weight:600;white-space:nowrap;max-width:210px;overflow:hidden;text-overflow:ellipsis}
td.role{min-width:230px}
td.nowrap{white-space:nowrap;font-variant-numeric:tabular-nums;color:var(--muted)}
.pill{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:600;
      color:#fff;white-space:nowrap}
.pill.ghost{background:transparent;border:1px solid currentColor}
a{color:var(--accent)}
a.ext{text-decoration:none;font-size:15px;opacity:.75}
a.ext:hover{opacity:1}
.detail td{background:var(--bg);padding:0}
.detail .inner{padding:14px 16px;display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:14px}
.blk h4{margin:0 0 5px;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.blk p{margin:0;white-space:pre-wrap}
.blk.pros h4{color:#16a34a} .blk.cons h4{color:#dc2626}
.meta{display:flex;flex-wrap:wrap;gap:6px}
.tag{background:var(--chip);border-radius:6px;padding:3px 8px;font-size:11px;color:var(--muted)}
.tag b{color:var(--ink);font-weight:600}
.empty{padding:56px 20px;text-align:center;color:var(--muted)}
footer{margin-top:22px;font-size:11px;color:var(--muted);text-align:center}
@media (max-width:640px){.wrap{padding:12px 10px 48px}.filters{padding:10px}input[type=search]{min-width:150px}}
"""

JS = r"""
const STATUS = __STATUS__, FIT = __FIT__, ROWS = __ROWS__, OPEN = __OPEN__;
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

// Status is a multi-select. The landing view is everything EXCEPT discarded --
// the discard pile is 500+ rows of dead postings and would bury the live ones.
const DEFAULT_OFF = ["discarded"];
let sortKey = "date_found", sortDir = -1;
const expanded = new Set();

const statusBoxes = () => [...document.querySelectorAll(".chk input[data-st]")];
const activeStatuses = () =>
  new Set(statusBoxes().filter((b) => b.checked).map((b) => b.dataset.st));

function setStatuses(keys) {
  const want = new Set(keys);
  statusBoxes().forEach((b) => { b.checked = want.has(b.dataset.st); });
}

const defaultStatuses = () =>
  statusBoxes().map((b) => b.dataset.st).filter((s) => !DEFAULT_OFF.includes(s));

const meta = (map, k) => map[k] || { label: k || "-", color: "#94a3b8" };

function fillSelect(sel, values, allLabel) {
  sel.innerHTML = `<option value="">${allLabel}</option>` +
    values.map((v) => `<option value="${esc(v)}">${esc(v)}</option>`).join("");
}

function uniq(field) {
  return [...new Set(ROWS.map((r) => r[field]).filter(Boolean))].sort((a, b) =>
    a.localeCompare(b, "es"));
}

function matches(r, statuses) {
  if (!statuses.has(r.status)) return false;

  const fit = $("#f-fit").value;
  if (fit && r.fit !== fit) return false;
  for (const [id, field] of [["#f-role", "role_type"], ["#f-mod", "modality"],
                             ["#f-type", "_bucket"], ["#f-src", "source"]]) {
    const v = $(id).value;
    if (v && r[field] !== v) return false;
  }
  const from = $("#f-from").value, to = $("#f-to").value;
  if (from && (!r.date_found || r.date_found < from)) return false;
  if (to && (!r.date_found || r.date_found > to)) return false;

  const q = $("#f-q").value.trim().toLowerCase();
  if (q) {
    const hay = [r.company, r.role, r.sector, r.pros, r.cons, r.notes,
                 r.location, r.comp, r.company_type].join(" ").toLowerCase();
    if (!q.split(/\s+/).every((t) => hay.includes(t))) return false;
  }
  return true;
}

const FIT_ORDER = { high: 3, medium: 2, low: 1, "": 0 };
const val = (r, k) => (k === "fit" ? (FIT_ORDER[r.fit] ?? 0) : (r[k] || "").toLowerCase());

// Default view is newest-found first, then best fit within the same day -- so the
// top of the table is always "what came in today, best first".
function sorted(list) {
  return list.slice().sort((a, b) => {
    const x = val(a, sortKey), y = val(b, sortKey);
    if (x < y) return -sortDir;
    if (x > y) return sortDir;
    if (sortKey !== "fit") {                      // secondary: fit, best first
      const fa = FIT_ORDER[a.fit] ?? 0, fb = FIT_ORDER[b.fit] ?? 0;
      if (fa !== fb) return fb - fa;
    } else {                                      // sorting by fit: newest first
      const da = a.date_found || "", db = b.date_found || "";
      if (da !== db) return da < db ? 1 : -1;
    }
    return (a.company || "").localeCompare(b.company || "", "es");
  });
}

function tag(label, value) {
  return value ? `<span class="tag"><b>${esc(label)}:</b> ${esc(value)}</span>` : "";
}

function detailRow(r) {
  const blocks = [
    r.pros ? `<div class="blk pros"><h4>Pros</h4><p>${esc(r.pros)}</p></div>` : "",
    r.cons ? `<div class="blk cons"><h4>Contras</h4><p>${esc(r.cons)}</p></div>` : "",
    r.notes ? `<div class="blk"><h4>Notas</h4><p>${esc(r.notes)}</p></div>` : "",
  ].join("");
  const tags = [
    tag("Ubicación", r.location), tag("Modalidad", r.modality), tag("Comp", r.comp),
    tag("Inglés", r.english_req), tag("Tipo", r.company_type), tag("Sector", r.sector),
    tag("Fuente", r.source), tag("Aplicado", r.date_applied),
    tag("CV", r.cv_file), tag("Carta", r.cover_letter_file), tag("Contacto", r.contact),
  ].join("");
  const inner = (blocks || tags)
    ? `<div class="inner">${blocks}${tags ? `<div class="blk"><h4>Detalle</h4><div class="meta">${tags}</div></div>` : ""}</div>`
    : `<div class="inner"><div class="blk"><p style="color:var(--muted)">Sin datos cargados todavía para esta fila.</p></div></div>`;
  return `<tr class="detail"><td colspan="9">${inner}</td></tr>`;
}

function render() {
  const statuses = activeStatuses();
  const list = sorted(ROWS.filter((r) => matches(r, statuses)));
  const body = list.map((r) => {
    const st = meta(STATUS, r.status), ft = meta(FIT, r.fit);
    const isOpen = expanded.has(r.id);
    const links = [
      r.posting_url ? `<a class="ext" href="${esc(r.posting_url)}" target="_blank" rel="noopener noreferrer" title="Ver posting">🔗</a>` : "",
      r.company_url ? `<a class="ext" href="${esc(r.company_url)}" target="_blank" rel="noopener noreferrer" title="Sitio de la empresa">🏢</a>` : "",
    ].join(" ");
    return `<tr class="row ${isOpen ? "open" : ""}" data-id="${esc(r.id)}">
      <td class="nowrap">${esc(r.date_found || "—")}</td>
      <td class="co" title="${esc(r.company)}">${esc(r.company || "—")}</td>
      <td class="role">${esc(r.role || "—")}</td>
      <td><span class="pill" style="background:${ft.color}">${esc(ft.label)}</span></td>
      <td><span class="pill" style="background:${st.color}">${esc(st.label)}</span></td>
      <td class="nowrap">${esc(r.last_update || "—")}</td>
      <td class="nowrap">${esc(r.modality || "—")}</td>
      <td class="nowrap">${esc(r.company_type || "—")}</td>
      <td class="nowrap">${links || "—"}</td>
    </tr>` + (isOpen ? detailRow(r) : "");
  }).join("");

  $("#tbody").innerHTML = body ||
    `<tr><td colspan="9"><div class="empty">Ningún puesto coincide con estos filtros.</div></td></tr>`;
  $("#count").textContent = `${list.length} de ${ROWS.length}`;
  document.querySelectorAll("th[data-k]").forEach((th) => {
    const on = th.dataset.k === sortKey;
    th.querySelector(".arrow").textContent = on ? (sortDir === 1 ? "▲" : "▼") : "";
  });
  // A card reads as pressed when its status is the only one showing.
  const on = activeStatuses();
  document.querySelectorAll(".card").forEach((c) => {
    const m = c.dataset.mode;
    const pressed = m === "all" ? on.size === Object.keys(STATUS).length
      : m === "open" ? OPEN.every((s) => on.has(s)) && on.size === OPEN.length
      : on.size === 1 && on.has(m);
    c.setAttribute("aria-pressed", String(pressed));
  });
  window.__filtered = list;
}

function exportCsv() {
  const cols = ["date_found", "company", "role", "fit", "status", "modality", "company_type",
                "location", "comp", "english_req", "posting_url", "company_url", "pros", "cons", "notes"];
  const q = (v) => `"${String(v ?? "").replace(/"/g, '""')}"`;
  const csv = [cols.join(",")]
    .concat((window.__filtered || []).map((r) => cols.map((c) => q(r[c])).join(",")))
    .join("\n");
  const url = URL.createObjectURL(new Blob(["﻿" + csv], { type: "text/csv;charset=utf-8" }));
  const a = document.createElement("a");
  a.href = url; a.download = "job-pipeline-filtrado.csv"; a.click();
  URL.revokeObjectURL(url);
}

function init() {
  fillSelect($("#f-role"), uniq("role_type"), "Todos los tipos");
  fillSelect($("#f-mod"), uniq("modality"), "Toda modalidad");
  fillSelect($("#f-type"), uniq("_bucket"), "Todo tipo de empresa");
  fillSelect($("#f-src"), uniq("source"), "Toda fuente");

  // Card = "show only this status" (click again to go back to the default view).
  document.querySelectorAll(".card").forEach((c) =>
    c.addEventListener("click", () => {
      const m = c.dataset.mode, on = activeStatuses();
      if (m === "all") setStatuses(Object.keys(STATUS));
      else if (m === "open") setStatuses(OPEN);
      else if (on.size === 1 && on.has(m)) setStatuses(defaultStatuses());
      else setStatuses([m]);
      render();
    }));
  document.querySelectorAll(".chk input[data-st]").forEach((b) =>
    b.addEventListener("change", render));
  document.querySelectorAll(".presets button").forEach((b) =>
    b.addEventListener("click", () => {
      const p = b.dataset.preset;
      setStatuses(p === "all" ? Object.keys(STATUS) : p === "open" ? OPEN
                : p === "none" ? [] : defaultStatuses());
      render();
    }));
  document.querySelectorAll("th[data-k]").forEach((th) =>
    th.addEventListener("click", () => {
      const k = th.dataset.k;
      if (sortKey === k) sortDir = -sortDir; else { sortKey = k; sortDir = -1; }
      render();
    }));
  $("#tbody").addEventListener("click", (e) => {
    if (e.target.closest("a")) return;               // let the link win
    const tr = e.target.closest("tr.row");
    if (!tr) return;
    const id = tr.dataset.id;
    expanded.has(id) ? expanded.delete(id) : expanded.add(id);
    render();
  });
  ["#f-fit", "#f-role", "#f-mod", "#f-type", "#f-src", "#f-from", "#f-to"]
    .forEach((s) => $(s).addEventListener("change", render));
  $("#f-q").addEventListener("input", render);
  $("#reset").addEventListener("click", () => {
    expanded.clear();
    sortKey = "date_found"; sortDir = -1;
    setStatuses(defaultStatuses());
    ["#f-fit", "#f-role", "#f-mod", "#f-type", "#f-src", "#f-from", "#f-to", "#f-q"]
      .forEach((s) => ($(s).value = ""));
    render();
  });
  $("#export").addEventListener("click", exportCsv);
  setStatuses(defaultStatuses());
  render();
}
document.addEventListener("DOMContentLoaded", init);
"""


def build(rows: list[dict], generated: str) -> str:
    counts = {k: sum(1 for r in rows if r.get("status") == k) for k in STATUS_META}
    open_n = sum(counts[k] for k in OPEN_STATUSES)

    cards = [("open", "Abiertos", open_n, "#4f46e5")]
    for key in ["new", "interested", "applied", "interviewing", "offer", "rejected", "discarded"]:
        cards.append((key, STATUS_META[key]["label"], counts.get(key, 0), STATUS_META[key]["color"]))
    cards.append(("all", "Todos", len(rows), "#94a3b8"))

    card_html = "\n".join(
        f'<button class="card" data-mode="{mode}" style="--c:{color}" aria-pressed="false">'
        f'<div class="n">{n}</div><div class="l">{label}</div></button>'
        for mode, label, n, color in cards
    )

    headers = [
        ("date_found", "Encontrado"), ("company", "Empresa"), ("role", "Rol"),
        ("fit", "Fit"), ("status", "Estado"), ("last_update", "Actualizado"),
        ("modality", "Modalidad"), ("company_type", "Tipo"), ("", "Links"),
    ]
    th_html = "\n".join(
        f'<th data-k="{k}">{lbl} <span class="arrow"></span></th>' if k else f"<th>{lbl}</th>"
        for k, lbl in headers
    )

    fit_opts = "".join(
        f'<option value="{k}">{v["label"]}</option>' for k, v in FIT_META.items() if k
    )

    # One checkbox per status, ordered along the lifecycle. Discarded ships
    # unchecked (DEFAULT_OFF in the JS) so the 500-row discard pile stays out of
    # the way until it is asked for.
    status_order = ["new", "interested", "applied", "interviewing", "offer", "hired",
                    "rejected", "no_response", "withdrawn", "discarded"]
    checks = "\n".join(
        f'<label class="chk"><input type="checkbox" data-st="{k}">'
        f'<span class="dot" style="background:{STATUS_META[k]["color"]}"></span>'
        f'{STATUS_META[k]["label"]} <b>{counts.get(k, 0)}</b></label>'
        for k in status_order if counts.get(k, 0) or not rows
    )

    script = (
        JS.replace("__STATUS__", embed(STATUS_META))
        .replace("__FIT__", embed(FIT_META))
        .replace("__ROWS__", embed(rows))
        .replace("__OPEN__", embed(OPEN_STATUSES))
    )

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Job Pipeline</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>🔍 Job Pipeline</h1>
    <span class="sub">{len(rows)} puestos · {open_n} abiertos · generado {generated}</span>
  </header>

  <div class="cards">{card_html}</div>

  <fieldset class="panel statusbox" style="margin-bottom:14px">
    <legend>Estado</legend>
    {checks}
    <span class="spacer"></span>
    <div class="presets">
      <button data-preset="default">Por defecto</button>
      <button data-preset="open">Abiertos</button>
      <button data-preset="all">Todos</button>
      <button data-preset="none">Ninguno</button>
    </div>
  </fieldset>

  <div class="panel filters">
    <label>Buscar<input type="search" id="f-q" placeholder="empresa, rol, pros, contras…"></label>
    <label>Fit<select id="f-fit"><option value="">Todo fit</option>{fit_opts}</select></label>
    <label>Tipo de rol<select id="f-role"></select></label>
    <label>Modalidad<select id="f-mod"></select></label>
    <label>Empresa<select id="f-type"></select></label>
    <label>Fuente<select id="f-src"></select></label>
    <label>Desde<input type="date" id="f-from"></label>
    <label>Hasta<input type="date" id="f-to"></label>
    <span class="spacer"></span>
    <span class="count" id="count"></span>
    <button class="btn" id="reset">Reiniciar</button>
    <button class="btn" id="export">Exportar CSV</button>
  </div>

  <div class="panel tablewrap">
    <table>
      <thead><tr>{th_html}</tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>

  <footer>Clic en una fila para ver pros, contras y detalle · fuente: <code>job-search/pipeline.csv</code> ·
  regenerar con <code>python tools/build_dashboard.py</code></footer>
</div>
<script>{script}</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", nargs="?", default=None)
    parser.add_argument("--template", action="store_true",
                        help="render the empty shell instead of the real data")
    parser.add_argument("--source", default=None, help="path to a pipeline CSV")
    args = parser.parse_args()

    rows = [] if args.template else load_rows(Path(args.source) if args.source else PIPELINE)
    if not args.template and not rows:
        print(f"warning: no rows found in {PIPELINE} - run tools/sync_pipeline.py first",
              file=sys.stderr)

    out = Path(args.out) if args.out else (
        WS / "dashboard.template.html" if args.template else DEFAULT_OUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(rows, datetime.now().strftime("%Y-%m-%d %H:%M")), encoding="utf-8")

    open_n = sum(1 for r in rows if r.get("status") in OPEN_STATUSES)
    print(f"dashboard: {out}  ({len(rows)} rows, {open_n} open)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
