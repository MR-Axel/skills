# skills

16 skills abiertos para [Claude Code](https://claude.com/claude-code). Cada carpeta es
independiente: copiás la que querés y funciona sola.

Lo que tienen en común no es el tema, es cómo están escritos. Ninguno trae tu stack, tu
producto ni tus preferencias cableados adentro. Te preguntan una vez, guardan la respuesta
en un archivo de tu repo que podés editar, y si ese archivo no está **te lo dicen en vez de
adivinar**. Un skill que adivina tu stack escribe código que parece razonable y no sigue
ninguna de tus convenciones, y eso cuesta más que no tener el skill.

> **English**: 16 open Claude Code skills for development, marketing and remote job
> hunting. Each directory is self-contained. Nothing is hardcoded: skills interview you
> once, store the answers in a config file in your repo, and stop and say so when that file
> is missing rather than guessing. Skill docs are in English; two skills
> (`linkedin-personal-brand`, and the reports of `latam-job-search`) work in Spanish.

## Desarrollo

Trece skills que cubren el ciclo completo. Comparten un archivo de config,
`.claude/project-profile.md`, que genera `project-setup`.

**Empezá por acá.**

| Skill | Qué hace |
|-------|----------|
| [project-setup](project-setup/) | **Corré este primero.** Detecta lo que puede de tu repo (package.json, lockfile, CI, estructura), te pregunta el resto mostrándote la evidencia, y escribe el perfil compartido. Una vez por proyecto. |

**Construir**

| Skill | Qué hace |
|-------|----------|
| [dev](dev/) | Implementa una feature o arregla un bug siguiendo las convenciones de tu repo. Reporta lo que asumió y lo que dejó afuera. |
| [ship](ship/) | Todo el circuito de una feature: planificar, implementar, validar, revisar, desplegar. Encadena a los demás. |
| [feature-agents](feature-agents/) | Lo mismo que `ship` pero **delegado a cinco subagentes** con herramientas acotadas: el que escribe el spec no puede escribir código, el que planifica no puede correr comandos. Para cambios grandes, donde la disciplina de fases deja de sostenerse sola. |

**Verificar**

| Skill | Qué hace |
|-------|----------|
| [test](test/) | Corre tu pipeline de validación y reporta honestamente qué pasó, qué falló y qué se salteó. Nunca marca en verde algo que no corrió, y distingue el check que analiza del que **ejecuta**. |
| [review](review/) | Code review de un diff. Cada hallazgo anclado a un archivo y línea reales, con el escenario de falla concreto. |
| [deep-review](deep-review/) | Review de arquitectura interactivo. Cada issue con opciones y su esfuerzo, riesgo e impacto. Vos priorizás, no él. |
| [ux](ux/) | Auditoría de UI: accesibilidad, responsive, estados de interacción y consistencia con tu design system. |
| [product](product/) | Review de negocio: ¿resuelve la necesidad, los gates aguantan, el flujo está completo, se encuentra? |

**Desplegar y después**

| Skill | Qué hace |
|-------|----------|
| [deploy](deploy/) | Pipeline de release. Permisos separados para commit, push y deploy, y nunca despliega un build que no pasó. |
| [deploy-qa](deploy-qa/) | QA **después** del deploy. Lee el diff, lo mapea al alcance real y elige la profundidad por blast radius en vez de correr siempre el mismo checklist. Arranca probando que el build nuevo esté de verdad en el aire. |
| [decision-log](decision-log/) | Bitácora de las decisiones que no se recuperan leyendo el código: por qué ese límite, por qué ese modelo, qué se descartó y por qué. La entrada va en el mismo commit que la implementa. |
| [design-system](design-system/) | Establece un design system donde no hay, y **hace cumplir** el que existe: cuatro gates que hacen que violarlo falle un check en vez de sobrevivir el review. |

### Cuál de los parecidos

Cuatro pares se pisan a propósito. La diferencia:

- **`ship` o `feature-agents`**: `ship` es un contexto haciendo todas las fases. `feature-agents` reparte las fases entre cinco subagentes con herramientas acotadas, así la separación es física y no disciplina. Cambio chico o mediano, `ship`. Cambio grande, `feature-agents`.
- **`review` o `deep-review`**: `review` es un portón sobre un diff, rápido y con veredicto. `deep-review` es una conversación sobre el sistema, sin veredicto, para el momento previo a un refactor.
- **`test` o `deploy-qa`**: `test` corre antes, sobre tu máquina. `deploy-qa` corre después, contra lo que quedó publicado.
- **`ux` o `design-system`**: `ux` audita una pantalla. `design-system` audita el sistema de tokens y arma los gates para que no se degrade.

## Marketing

| Skill | Qué hace |
|-------|----------|
| [community-manager](community-manager/) | Contenido listo para publicar en X, LinkedIn, Instagram y más, sobre tu propio brand profile y tu funnel. **Nunca inventa métricas, testimonios ni social proof**: deja placeholders y te los lista al final. |
| [linkedin-personal-brand](linkedin-personal-brand/) | Marca personal en LinkedIn, no de producto. Te entrevista para saber a qué apuntás y en qué sos bueno, rastrea las fuentes primarias de **tu** disciplina y devuelve textos listos para publicar o comentar. Mide qué funcionó post a post. Cuatro rutinas automatizables. En español. |

`community-manager` es para la marca de tu producto o tu funnel. `linkedin-personal-brand`
es para vos como persona: tu nombre, tu criterio, tu nicho.

## Búsqueda laboral

| Skill | Qué hace |
|-------|----------|
| [latam-job-search](latam-job-search/) | Búsqueda de trabajo remoto para candidatos en LatAm. Filtra por modalidad, país elegible, huso horario, piso salarial, idioma, tipo de empresa y rubro **antes** de evaluar el fit, porque eso es lo que realmente te descarta. Incluye dos CLIs de portales sin API key. |

## Instalación

```bash
git clone https://github.com/MR-Axel/skills.git
mkdir -p ~/.claude/skills
cp -r skills/<nombre-del-skill> ~/.claude/skills/
```

Para llevarlos todos de una vez:

```bash
cp -r skills/*/ ~/.claude/skills/
```

`~/.claude/skills/` los deja disponibles en todos tus proyectos. `.claude/skills/` dentro
de un repo los deja solo ahí. Claude Code los detecta solo: invocalos por nombre
(`/review`) o pedí lo que necesitás en lenguaje natural.

Algunos tienen un paso extra, está en el README de cada uno. `latam-job-search` necesita
[bun](https://bun.sh) para sus dos CLIs; sin bun funciona igual con búsqueda web y lo
aclara en la salida.

**Para los de desarrollo, empezá con `/project-setup`.** Sin el perfil los demás no
arrancan, y eso es a propósito.

## Principios

Cuatro reglas, y son la razón por la que estos skills están en un repo y no sueltos:

1. **Preguntar antes de asumir.** Un skill que infiere tu stack o tus preferencias te va a
   dar resultados que ya descartaste. La config vive en tu repo, en un archivo que podés
   editar, no cableada adentro del skill.
2. **Mostrar lo que se filtró o se salteó.** Un filtro silencioso es indistinguible de un
   día sin resultados. Un check que no corrió no es un check que pasó.
3. **No fabricar.** Ni datos, ni contactos, ni métricas, ni testimonios, ni hallazgos sin
   archivo y línea. Si no se pudo verificar, se dice.
4. **Reportar honestamente.** Si los tests fallan, se dice y se pega la salida. Si el
   pipeline paró a la mitad, se dice dónde y en qué estado quedó todo.

## Privacidad

Ningún skill manda datos a ningún lado. Todo lo que aprenden queda en archivos dentro de tu
workspace. Qué genera cada uno, y qué hacer con eso:

| Archivo | Lo genera | ¿Commitear? |
|---------|-----------|-------------|
| `.claude/project-profile.md` | `project-setup` | **Sí**, así el equipo comparte el mismo comportamiento. Revisalo antes: nunca debe tener secretos, keys ni identificadores de infraestructura. Referenciá el nombre de la variable de entorno, no el valor. `project-setup` rechaza el valor si se lo pasás. |
| `DECISIONS.md` | `decision-log` | **Sí**, ese es el punto: la entrada va en el mismo commit que la decisión. |
| `.claude/lessons.md` | `ship` | A gusto. No tiene datos sensibles. |
| `.claude/brand-profile.md` | `community-manager` | A gusto. Es posicionamiento, no credenciales. |
| `perfil-marca.md` | `linkedin-personal-brand` | A gusto. |
| `job-search/` | `latam-job-search` | **No.** Tiene tus números de sueldo y tu historial de postulaciones. Va al `.gitignore`. |

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md). Issues y PRs bienvenidos, en español o inglés.

## Licencia

MIT, ver [LICENSE](LICENSE). Un skill incluye código de terceros con su propia atribución,
ver [NOTICE.md](NOTICE.md).
