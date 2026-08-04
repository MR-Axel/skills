# Contribuir

Issues y PRs bienvenidos, en español o inglés.

## Agregar un skill

Cada skill es una carpeta de primer nivel, autocontenida. La estructura mínima:

```
mi-skill/
├── SKILL.md      frontmatter con name, description, allowed-tools, y las instrucciones
└── README.md     qué hace, cómo se instala, qué genera
```

Si el skill crece, separá el detalle en `references/` y dejá el `SKILL.md` como índice.
Archivos de apoyo (templates, ejemplos) van en `assets/`. Ejecutables en `tools/`.

### El frontmatter

```yaml
---
name: mi-skill
description: >
  Qué hace, en una o dos oraciones, seguido de las frases que deberían dispararlo.
  Incluí triggers en los dos idiomas si el skill es para LatAm.
license: MIT
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch
---
```

`description` es lo único que Claude ve antes de decidir si carga el skill. Escribila
pensando en eso: qué problema resuelve y con qué palabras lo va a pedir alguien.

Acotá `allowed-tools` a lo que el skill realmente usa. Si necesita `Bash`, restringí el
patrón (`Bash(bun run *cli.ts *)`) en vez de habilitarlo entero.

## Reglas de estilo

- **Preguntar antes de asumir.** Si el skill necesita saber algo del usuario, que lo
  pregunte con opciones concretas. Un default silencioso es una decisión tomada por otro.
- **Mostrar lo que se filtró o se omitió.** Un skill que descarta cosas sin decirlo es
  imposible de depurar desde afuera.
- **No fabricar.** Nada de datos, contactos o resultados inventados. Si no se pudo
  verificar, se dice.
- **Sin datos personales.** Ningún skill de este repo lleva datos de nadie adentro. Todo
  lo específico de una persona vive en archivos que genera el skill en el workspace del
  usuario, y esos archivos van al `.gitignore`.
- **Sin em dashes.** Preferí comas, dos puntos o paréntesis.

## Código de terceros

Si incorporás código con otra licencia, agregá la atribución a `NOTICE.md` con el link al
original y el texto de la licencia. No lo mezcles adentro del skill sin declararlo.

## Antes del PR

- Probá el skill de punta a punta al menos una vez, incluido el onboarding si tiene.
- Verificá que no quedaron datos personales: `grep -riE "<tu nombre>|<tu email>" mi-skill/`
- Actualizá la tabla de skills en el README raíz.
