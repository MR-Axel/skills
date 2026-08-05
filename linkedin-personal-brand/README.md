# linkedin-personal-brand

Sistema de marca personal en LinkedIn para [Claude Code](https://claude.com/claude-code).

Define tu identidad y tu voz, arma un calendario, rastrea todos los días las noticias de tu
nicho y te devuelve texto listo para publicar o comentar, y mide qué funcionó post a post.

Sirve igual si buscás trabajo, si querés clientes, si buscás inversión o si querés que tu nombre
suene en tu área. La primera vez que lo usás te entrevista para saber hacia dónde apuntar la
investigación.

> Personal branding system for LinkedIn. Interviews you first, then researches your niche daily
> and drafts ready-to-post copy. Spanish content, works in English too.

## Instalación

```bash
git clone https://github.com/MR-Axel/skills.git
mkdir -p ~/.claude/skills
cp -r skills/linkedin-personal-brand ~/.claude/skills/
```

En Windows, la ruta global es `C:\Users\<usuario>\.claude\skills\`.

Reiniciá Claude Code después de copiar.

## Uso

Creá una carpeta donde quieras que vivan tus archivos de marca y trabajá ahí. La primera vez:

```
/linkedin-personal-brand
```

Te hace el onboarding (objetivo, terreno, audiencia, idioma, ritmo, restricciones y tono) y crea
`perfil-marca.md`. A partir de ahí lee ese perfil solo, sin repetir preguntas.

Después le pedís cosas en lenguaje natural:

- "buscame de qué hablar hoy"
- "armame el calendario de publicación"
- "escribí la postura de mañana"
- "cargá estas métricas del post de ayer"
- "por qué te parece que rindió así"

## La app del calendario

Todo lo que se prepara entra en una cola con fecha, hora, texto completo, prompt de imagen y
links de fuente. `assets/calendario-app.html` la muestra en un solo archivo, sin dependencias y
sin servidor. Se abre con doble clic.

```
Copiá assets/calendario-app.html a mi carpeta y cargale la cola del calendario
```

Tres vistas:

- **Semana**: la grilla de días con el formato que le toca a cada uno, para ver un hueco antes de
  que sea tarde.
- **Todo**: la cola completa por fecha, con la cuarentena al final.
- **Publicados**: la tabla de rendimiento, un post por fila, con el engagement de terceros
  calculado sobre alcanzados. Si terminás comparando un post medido a 3hs contra otro medido a
  24hs, la app te avisa: son cortes que no se pueden comparar entre sí.

Click en cualquier post abre el detalle, con el texto y el prompt de imagen listos para copiar,
las fuentes para el primer comentario, la cuenta regresiva si tiene fecha límite, y la evolución
entre cortes si ya está publicado.

**Guardala en los marcadores del navegador.** Es lo que hace que el sistema se sostenga: si la
cola no está a un clic de distancia, se deja de mirar a la tercera semana y las ideas preparadas
se pierden. Arrastrá el archivo a la barra de marcadores, o abrilo y guardalo con Ctrl+D
(Cmd+D en Mac).

Claude escribe los datos en el bloque JSON que la app trae adentro. Para actualizarla, reescribe
solo ese bloque, así podés bajar una versión nueva de la app del repo sin perder tus datos.

## Automatizarlo

En `routines/` hay cuatro rutinas listas para instalar como tareas programadas: el radar diario y
tres de preparación de contenido, cada una corriendo el día antes del post que prepara.

Completá los marcadores entre corchetes de cada archivo con tu carpeta, tu día y tu franja
horaria, y después pedile a Claude Code que las programe:

> Creá una tarea programada que corra todos los días a las 8am con el contenido de
> `routines/radar-diario.md`

Instalá solo las que correspondan a tu calendario. Ver `routines/README.md`.

## Qué hace y qué no

**Hace:** investiga en fuentes primarias de tu área, redacta textos completos listos para pegar,
te dice a qué categoría pertenece cada cosa (post propio, comentario en post ajeno, o material
para más adelante), y lleva el registro de métricas con sus hipótesis.

**No hace:** publicar ni comentar por vos. Todo lo produce para que vos decidas y ejecutes.

**No lee tu feed de LinkedIn.** Eso necesita una sesión autenticada. La investigación es por
búsqueda web sobre fuentes públicas, y el skill lo declara en vez de simular que vio tu feed.

## Estructura

```
linkedin-personal-brand/
  SKILL.md
  references/
    01-onboarding.md          la entrevista inicial
    02-fuentes-por-area.md    qué rastrear según tu disciplina
    03-radar-diario.md        cómo convertir noticias en contenido
    04-metricas.md            cómo leer los números sin engañarte
    05-calendario-editorial.md  la cola de producción y la app
    plantillas.md             plantillas de los archivos que mantiene
  routines/
    radar-diario.md
    prep-serie.md
    prep-postura.md
    prep-historia.md
  assets/
    calendario-app.html       la app de la cola, un archivo sin dependencias
  README.md
```

## Privacidad

Todo queda en archivos dentro de tu carpeta de trabajo. Nada se manda a ningún lado.

`perfil-marca.md` e `identidad-marca.md` contienen información personal y criterios que
probablemente no quieras públicos. Si tu carpeta de marca vive en un repo, agregalos al
`.gitignore`.

## Un consejo antes de empezar

Contestá el onboarding con honestidad, sobre todo dos preguntas: cuántos días por semana podés
publicar **de verdad**, y qué tipo de post te da vergüenza ajena.

Sostener dos posts por semana durante seis meses vale más que cinco por semana durante tres
semanas. Y saber qué no querés parecer define tu voz mejor que cualquier adjetivo.
