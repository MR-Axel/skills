# skills

Skills para [Claude Code](https://claude.com/claude-code), abiertos y listos para copiar.
Cada carpeta es un skill independiente.

> Open Claude Code skills. Each directory is self-contained.

## Skills

### Búsqueda laboral

| Skill | Qué hace |
|-------|----------|
| [latam-job-search](latam-job-search/) | Búsqueda de trabajo remoto para candidatos en LatAm. Filtra por modalidad, país elegible, huso horario, piso salarial, idioma y rubro **antes** de evaluar el fit. Incluye dos CLIs de portales sin API key. |

### Desarrollo

Estos comparten un archivo de config, `.claude/project-profile.md`, que genera
`project-setup`. Ninguno asume tu stack: si el perfil no existe, te lo dicen en vez de
adivinar y escribir código que no sigue tus convenciones.

| Skill | Qué hace |
|-------|----------|
| [project-setup](project-setup/) | **Corré este primero.** Detecta lo que puede de tu repo, te pregunta el resto y escribe el perfil compartido. Una vez por proyecto. |
| [dev](dev/) | Implementa una feature o arregla un bug siguiendo las convenciones de tu repo. Reporta lo que asumió y lo que dejó afuera. |
| [test](test/) | Corre tu pipeline de validación y reporta honestamente qué pasó, qué falló y qué se salteó. Nunca marca en verde algo que no corrió. |
| [review](review/) | Code review de un diff. Cada hallazgo anclado a un archivo y línea reales, con el escenario de falla concreto. |
| [deep-review](deep-review/) | Review de arquitectura interactivo. Cada issue con opciones y su esfuerzo, riesgo e impacto. Vos priorizás, no él. |
| [ux](ux/) | Auditoría de UI: accesibilidad, responsive, estados de interacción y consistencia con tu design system. |
| [deploy](deploy/) | Pipeline de release. Respeta permisos separados para commit, push y deploy, y nunca despliega un build que no pasó. |
| [ship](ship/) | Todo el circuito de una feature: planificar, implementar, validar, revisar, desplegar. Encadena los anteriores. |
| [feature-agents](feature-agents/) | Lo mismo que `ship` pero **delegado a cinco subagentes** con herramientas acotadas: el que escribe el spec no puede escribir código, el que planifica no puede correr comandos. Para cambios grandes, donde la disciplina de fases deja de sostenerse sola. |
| [deploy-qa](deploy-qa/) | QA **después** del deploy. Lee el diff, lo mapea al alcance real y elige la profundidad por blast radius en vez de correr siempre el mismo checklist. Arranca probando que el build nuevo esté de verdad en el aire. |
| [decision-log](decision-log/) | Bitácora de las decisiones que no se recuperan leyendo el código: por qué ese límite, por qué ese modelo, qué se descartó y por qué. La entrada va en el mismo commit que la implementa. |
| [product](product/) | Review de negocio: ¿resuelve la necesidad, los gates aguantan, el flujo está completo, se encuentra? |

### Marketing

| Skill | Qué hace |
|-------|----------|
| [community-manager](community-manager/) | Contenido listo para publicar en X, LinkedIn, Instagram y más, sobre tu propio brand profile y tu funnel. **Nunca inventa métricas, testimonios ni social proof**: deja placeholders y te los lista. |
| [linkedin-personal-brand](linkedin-personal-brand/) | Marca personal en LinkedIn, no de producto. Te entrevista para saber a qué apuntás y en qué sos bueno, rastrea las fuentes primarias de **tu** disciplina y devuelve textos listos para publicar o comentar. Mide qué funcionó post a post. Cuatro rutinas automatizables. |

`community-manager` es para la marca de tu producto o tu funnel. `linkedin-personal-brand`
es para vos como persona: tu nombre, tu criterio, tu nicho.

## Instalación

```bash
git clone https://github.com/MR-Axel/skills.git
mkdir -p ~/.claude/skills
cp -r skills/<nombre-del-skill> ~/.claude/skills/
```

`~/.claude/skills/` los deja disponibles en todos tus proyectos. `.claude/skills/` dentro
de un repo los deja solo ahí. Claude Code los detecta solo: invocalos por nombre
(`/review`) o pedí lo que necesitás en lenguaje natural.

Algunos tienen un paso extra, está en el README de cada uno.

**Para los de desarrollo, empezá con `/project-setup`.** Sin el perfil los demás no
arrancan, y eso es a propósito.

## Principios

Los skills de este repo comparten cuatro reglas:

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

Ningún skill manda datos a ningún lado. Todo lo que aprenden queda en archivos dentro de
tu workspace.

Dos archivos de config merecen atención antes de commitearlos:

- `.claude/project-profile.md` **nunca** debe tener secretos, keys, tokens ni
  identificadores de infraestructura. Referenciá el nombre de la variable de entorno, no
  el valor. `project-setup` te lo avisa durante la entrevista y rechaza el valor si se lo
  pasás.
- `job-search/` (perfil, tracker) tiene tus números de sueldo y tu historial de
  postulaciones. Va al `.gitignore`.

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md). Issues y PRs bienvenidos, en español o inglés.

## Licencia

MIT, ver [LICENSE](LICENSE). Algunos skills incluyen código de terceros con su propia
atribución, ver [NOTICE.md](NOTICE.md).
