# feature-agents

Cinco subagentes especializados para una feature grande: spec, planner, tester, QA,
deployer. Cada uno con las herramientas que su trabajo necesita, y ninguna más.

> Five specialist subagents for one feature. The phase boundary is the tool list, not a
> promise in a prompt.

## Qué agrega sobre `/ship`

[`ship`](../ship/) corre el mismo arco en un solo contexto, y para la mayoría de los cambios
es lo correcto: menos overhead, menos handoffs, un hilo de pensamiento continuo.

Esto es para cuando el cambio es lo bastante grande como para que **la disciplina de fases
deje de sostenerse sola**. En un contexto único, la tracción hacia escribir código mientras
todavía estás entendiendo el requerimiento es fuerte, y lo que sale es un plan
ingenierizado hacia atrás desde una implementación a medio hacer.

La delegación lo hace estructuralmente imposible:

| Agente | Tiene | No puede |
|---|---|---|
| `feature-spec` | Read, Grep, Glob, AskUserQuestion | escribir un archivo, proponer arquitectura |
| `feature-planner` | Read, Grep, Glob | escribir, correr comandos |
| `feature-tester` | Read, Write, Edit, Bash, Grep, Glob | montar infra de tests que no existía |
| `feature-qa` | Read, Grep, Glob, Bash | editar código, pushear |
| `feature-deployer` | Read, Bash, Grep | correr sin un sí explícito del humano |

El spec writer no "se compromete" a no escribir código: no tiene con qué.

**Línea aproximada**: tres archivos o más, un cambio de schema, una integración, o cualquier
cosa donde equivocarse sea caro. Por debajo de eso, `ship`.

## Instalación

Son dos pasos, porque en Claude Code los agentes y los skills viven en carpetas distintas:

```bash
git clone https://github.com/MR-Axel/skills.git

# el skill
mkdir -p ~/.claude/skills
cp -r skills/feature-agents ~/.claude/skills/

# los agentes · van SIEMPRE dentro del repo, porque conocen sus convenciones
mkdir -p .claude/agents
cp skills/feature-agents/agents/*.md .claude/agents/
```

Necesita `.claude/project-profile.md`, el mismo perfil que usan los demás skills de
desarrollo. Si no lo tenés, corré [`/project-setup`](../project-setup/) primero: los
agentes planifican contra tus convenciones, y un plan sobre un stack adivinado es un plan
que vas a tirar.

## Uso

```
/feature-agents <lo que querés construir>
```

## Las tres reglas que lo sostienen

1. **Nunca implementar antes de un plan aprobado.** Si el usuario dice "dale, hacelo" sin
   mirar, mostrale el plan igual.
2. **Silencio no es aprobación.** El check humano espera un sí explícito. Si no llegó, no
   hay deploy.
3. **Si el plan estaba mal, volvés al plan.** Seguir escribiendo sobre un plan roto es cómo
   termina una feature que funciona y un código que no.

## El error de handoff más común

Resumir la salida de la fase anterior en vez de pasarla. Un spec comprimido a tres bullets
pierde justo la restricción que el planner necesitaba, y nadie se da cuenta hasta que el
plan vuelve sin ella.

## Memoria de incidentes

El planner lee `.claude/memory/incidents.md` antes de planear: las trampas que este repo ya
te tendió, para avisarte antes de que vuelvas a caer.

Es la pieza que hace que el kit mejore en vez de repetir. El formato y, sobre todo, **qué NO
va adentro**, están en [`references/incident-memory.md`](references/incident-memory.md).
Un archivo con todo adentro deja de leerse, y entonces vuelve a no existir.

## Datos

No manda nada a ningún lado. Lo único que genera es `.claude/memory/incidents.md` en tu
repo, que escribís vos. Commitealo: es conocimiento de equipo, no dato personal. Como
siempre, si un incidente involucra una credencial o un endpoint privado, escribí el
razonamiento sin el dato.
