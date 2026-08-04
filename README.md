# skills

Skills para [Claude Code](https://claude.com/claude-code), abiertos y listos para copiar.
Cada carpeta es un skill independiente: se instala sola, no depende de las otras.

> Open Claude Code skills. Each directory is a self-contained skill.

## Skills disponibles

| Skill | Qué hace | Idioma |
|-------|----------|--------|
| [latam-job-search](latam-job-search/) | Búsqueda de trabajo remoto para candidatos en LatAm. Filtra por modalidad, país elegible, huso horario, piso salarial y nivel de idioma **antes** de evaluar el fit. Incluye dos CLIs de portales sin API key. | ES / EN |

## Instalación

Todos los skills se instalan igual: copiás la carpeta a `~/.claude/skills/` para tenerlo
disponible en todos tus proyectos, o a `.claude/skills/` dentro de un repo para que viva
solo ahí.

```bash
git clone https://github.com/MR-Axel/skills.git
mkdir -p ~/.claude/skills
cp -r skills/<nombre-del-skill> ~/.claude/skills/
```

Después leé el README del skill: algunos tienen un paso extra (dependencias, un comando de
setup inicial).

Claude Code los detecta solo. Podés invocarlos por nombre (`/job-search`) o simplemente
pedir lo que necesitás en lenguaje natural.

## Principios

Los skills de este repo comparten tres reglas:

1. **Preguntar antes de asumir.** Un skill que infiere tus preferencias en vez de
   preguntarlas te va a dar resultados que ya descartaste. La entrevista inicial es corta,
   con opciones para clickear, y guarda lo que no quisiste contestar como pendiente en vez
   de inventar un default.
2. **Mostrar lo que se filtró.** Un filtro silencioso es indistinguible de un día sin
   resultados, y no podés corregir lo que no ves.
3. **No fabricar.** Nada de datos inventados, contactos inventados o credenciales
   infladas. Si el skill no pudo verificar algo, lo dice.

## Privacidad

Ningún skill de este repo manda datos a ningún lado. Todo lo que aprenden queda en
archivos dentro de tu workspace. Los READMEs indican cuáles conviene agregar al
`.gitignore`.

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md). Issues y PRs bienvenidos, en español o inglés.

## Licencia

MIT, ver [LICENSE](LICENSE). Algunos skills incluyen código de terceros con su propia
atribución, ver [NOTICE.md](NOTICE.md).
