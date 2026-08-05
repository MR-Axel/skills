# latam-job-search

Búsqueda de trabajo remoto para candidatos en LatAm. Filtra primero por lo que realmente
te descarta (modalidad, país elegible, huso horario, piso salarial, nivel de idioma) y
recién después evalúa el fit.

> Remote job search for LatAm-based candidates. Gates first, scoring second.
> English section below.

---

## El problema que resuelve

La mayoría de las herramientas de búsqueda laboral puntúan primero y verifican después.
Para alguien en LatAm eso significa leer una oferta perfecta que resulta ser:

- híbrida en otra ciudad, o híbrida cuando vos pediste 100% remoto
- "remote, globally" pero elegible solo en tres países que no incluyen el tuyo
- cotizada en una moneda que no aceptás, o por debajo de tu piso
- construida sobre llamadas diarias en un idioma que leés mejor de lo que hablás
- el mismo puesto que ya viste ayer, con otra URL
- de una consultora o una agencia de staffing, cuando vos querías trabajar en producto
- con un link del agregador que ya está muerto

Este skill invierte el orden. Cada filtro sale de una respuesta que diste en el onboarding,
no de una inferencia.

## Instalación

Necesitás [bun](https://bun.sh) para las dos CLIs de portales. Sin bun el skill funciona
igual, con `WebSearch` como fallback, y lo aclara en la salida.

```bash
git clone https://github.com/MR-Axel/skills.git
mkdir -p ~/.claude/skills
cp -r skills/latam-job-search ~/.claude/skills/
cd ~/.claude/skills/latam-job-search/tools/linkedin-search/cli && bun install
cd ../../freehire-search/cli && bun install
```

Para instalarlo solo en un proyecto, copiá la carpeta a `.claude/skills/` de ese repo.

Después, en Claude Code:

```
/job-setup
```

## Uso

| Comando | Qué hace |
|---------|----------|
| `/job-setup` | Entrevista de onboarding, escribe tu perfil. Una sola vez. |
| `/job-search` | Una corrida: busca, filtra, puntúa, deduplica, presenta. Acepta foco: `/job-search voice AI` |
| `/job-evaluate 3` | Evaluación completa de la oferta 3 del último listado |
| `/job-track` | Registra una postulación |
| `/job-dashboard` | Regenera el tablero HTML con todo lo visto hasta hoy |

También funciona en lenguaje natural: "buscá trabajo", "¿hay algo nuevo hoy?",
"¿esta oferta me sirve?".

Para correrlo todas las mañanas, armá una tarea programada que invoque `/job-search`.

## Qué te pregunta el onboarding

Siete rondas cortas, con opciones para clickear y campo libre para lo específico. Las que
más cambian los resultados:

- **Modalidad**, y te avisa la consecuencia: si elegís 100% remoto, los híbridos
  desaparecen del listado, incluso los de tu propia ciudad
- **Qué países pueden contratarte de verdad**, y cuáles son un no automático
- **Tres números de plata**: objetivo, piso y punto de retiro, más un objetivo distinto
  por clase de empleador, porque una agencia de staffing y una empresa de US pagando en
  dólares no soportan el mismo número
- **Idiomas con nivel MCER y el corte escrito/hablado**, más qué hacer con puestos que
  exigen más de lo que tenés y son cara al cliente
- **Tipo de empresa, etapa y rubro**: startup temprana, scale-up, enterprise, consultora,
  agencia de staffing, empresa de PE, sector público. Y dos listas de rubros: los que
  querés y los que no. Un rubro rechazado se descarta, no se puntúa bajo
- **Lista de "nunca me muestres esto"**, que es la pregunta que casi ningún setup hace
- **Lista de "nunca afirmes esto"**, que después limita cualquier CV o carta que se escriba

## Qué genera

Todo queda en `job-search/` dentro de tu workspace:

```
job-search/
├── profile.md        tu perfil, editable a mano
├── seen_jobs.json    todo lo visto, presentado y descartado, con el motivo del descarte
├── tracker.csv       tus postulaciones
├── pipeline.csv      una fila por puesto, de "lo encontré" hasta "oferta" o "descartado"
└── dashboard.html    el tablero, generado desde pipeline.csv
```

Nada se envía a ningún lado. Si tu workspace es un repo, agregá `job-search/` al
`.gitignore`: el perfil tiene tus números de sueldo y el tracker tu historial.

## El tablero

Después de unas semanas el problema deja de ser encontrar ofertas y pasa a ser acordarte
cuál era cuál. La tabla de la mañana sirve esa mañana; a los quince días tenés doscientas
filas repartidas en veinte conversaciones y ninguna forma de ver en qué quedó cada una.

`pipeline.csv` es una fila por puesto con todo el ciclo de vida, y guarda lo que el scraper
no sabe: `pros`, `cons`, `location`, `modality`, `comp`, `english_req`, `company_type`,
`company_url`. `dashboard.html` lo renderiza en un archivo solo, sin servidor ni CDN, que
abrís directo del disco y anda offline.

```bash
python tools/sync_pipeline.py     # junta seen_jobs.json + tracker.csv en pipeline.csv
python tools/build_dashboard.py   # arma job-search/dashboard.html
```

- Estado como checkboxes múltiples, con **descartados apagado por defecto**: el descarte se
  vuelve la mayoría de las filas enseguida y taparía todo lo demás
- Filtros de fit, tipo de rol, modalidad, tipo de empresa, fuente y rango de fechas
- El buscador entra también adentro de pros y contras, así que "n8n" o "sin inglés hablado"
  encuentra la fila aunque no esté en el título
- Orden por defecto: fecha de encontrado, y dentro del mismo día el mejor fit primero
- Clic en una fila abre pros, contras, notas, comp, idioma y el CV que mandaste
- Exporta a CSV lo que estés viendo filtrado

> **Guardalo en marcadores.** Es un archivo local, así que arrastrá `job-search/dashboard.html`
> a la barra de marcadores del navegador (o abrilo y hacé Ctrl/Cmd+D). Tenerlo a un clic es
> la diferencia entre un tablero que mirás todos los días y uno que regenerás y no volvés a
> abrir. El `sync` es no destructivo: regenerar nunca te pisa lo que escribiste a mano, así
> que el marcador siempre apunta a la última versión.

`sync_pipeline.py` solo rellena campos vacíos y mueve el estado hacia adelante, nunca hacia
atrás. `last_update` se estampa únicamente en las filas que cambiaron de verdad, que es lo
que hace que esa columna signifique algo.

## Salida

```
# Job search, 2026-08-04

| # | Fit | Rol | Empresa | Link | Pros | Contras |
|---|-----|-----|---------|------|------|---------|

**Mejor match:** dos o tres líneas de por qué, y la cosa a chequear antes de aplicar.

Casi-matches (no listados): Empresa X, híbrido en Retiro.

Filtrado: 6 híbridos, 4 país equivocado, 2 bajo el piso, 1 rubro rechazado, 11 ya vistos.
Cobertura: 34 búsquedas en 2 portales. 425 ofertas nuevas guardadas.
```

La línea de "filtrado" no es decorativa: es la única forma de distinguir un día flojo de un
filtro demasiado agresivo, y de que puedas corregirlo.

---

## English

Remote job search for LatAm-based candidates. It runs hard gates (work modality, country
eligibility, timezone overlap, compensation floor, language level) **before** scoring any
posting, because those are what actually disqualify a remote candidate in this region.

Install by copying `latam-job-search/` into `~/.claude/skills/` (or a project's
`.claude/skills/`), running `bun install` in both `tools/*/cli` directories, and then
`/job-setup` in Claude Code.

The onboarding interview covers location and modality, work authorization, three
compensation numbers plus per-employer-class targets, per-language CEFR levels with a
written-vs-spoken split, priority role families, an explicit do-not-present list, a
never-claim list, watch-list companies, culture red-flag phrases, and output preferences.

Every gate is documented in `references/02-eligibility-and-location.md`, including why each
one exists. State lives in `job-search/` in your own workspace and is never transmitted.

`tools/sync_pipeline.py` and `tools/build_dashboard.py` turn that state into
`job-search/dashboard.html`: one self-contained offline page, one row per posting across
its whole lifecycle, with multi-select status filters (discarded off by default), search
that reaches into the pros and cons text, and CSV export of the current filter. Bookmark
the file — regenerating it never overwrites hand-written notes, so the bookmark always
points at the current view.

## Tools

Two `bun` CLIs, no API keys, no logins:

- `tools/linkedin-search` reads LinkedIn's public job board for any country or "Remote"
- `tools/freehire-search` queries the freehire.dev aggregator with region, country, skill
  and company facets

Both ship `search` and `detail` commands and emit JSON. LinkedIn's public pages are used
under a personal-use assumption: automated access is against their terms of service, so
keep volume low.

## Credits

The two portal CLIs and the original job-search framework they came from are by
[Mads Lorentzen](https://github.com/MadsLorentzen/ai-job-search), MIT licensed. The gates,
the onboarding interview and the run loop in this skill are new work built on top, licensed
MIT as well. See [NOTICE.md](../NOTICE.md).
