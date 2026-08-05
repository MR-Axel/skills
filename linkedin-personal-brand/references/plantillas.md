# Plantillas de archivos

Crear en el directorio de trabajo de la persona. Rellenar con lo que salga del onboarding y de
las sesiones, nunca con supuestos.

---

## perfil-marca.md

```markdown
# Perfil de marca · [nombre]

## Objetivo
Prioridad 1: [objetivo principal]
Prioridad 2: [secundario, si hay]
Cuando dos objetivos piden cosas distintas, manda el 1.

## Terreno
Especialidad: [específica, no "tecnología"]
Terreno secundario: [opcional]
Seniority y contexto: [años, si lidera, si emprende]
Proyectos propios: [nombre y qué resuelve cada uno]

## Audiencia
[a quién le habla y por qué]

## Idioma y mercado
Idioma principal: [x]
Segundo idioma y cuándo se usa: [x]
Mercado objetivo: [x]

## Ritmo sostenible
[días por semana que puede publicar de verdad]

## Restricciones duras
- Nunca usar procesos de selección en curso como material.
- [temas vedados]
- [empleadores o clientes que no se mencionan]
- [resultados que no hay que sobredimensionar]

## Tono
Referencia: [tipo de voz elegida]
Lo que le da vergüenza ajena: [para marcar el límite]
Manías tipográficas y de estilo: [ej. signos que no usa, formatos que evita]

## Fuentes del radar
[las de su área, de references/02-fuentes-por-area.md, más las propias]

## Estilo visual
Paleta: [hex]
Estilo de ilustración: [uno solo, sostenido, para que se lean como serie]
Formato: [proporción y tipo de imagen]
```

---

## identidad-marca.md

```markdown
# Identidad de marca

## Narrativa central
[Qué ve la persona que está mal y nadie arregla. Escrito en primera persona, sin currículum.
Es el texto del que salen todos los posts.]

## Por qué cada proyecto
[Motivación real, no de mercado. Uno por proyecto.]

## Posturas fuertes
[Tres a cinco. Una postura genera conversación; una opinión solo genera acuerdo. Si nadie
puede estar en desacuerdo, no es postura.]

## Cómo comunica
- [reglas propias de esta persona]

## Series y territorios propios
[Ángulos recurrentes que nadie más en el nicho usa. Es lo que la vuelve reconocible.]
```

---

## calendario.md

Es la cola de producción y la fuente de verdad. Se lee entero antes de proponer cualquier
contenido. Ver `05-calendario-editorial.md`.

````markdown
# Calendario editorial

**Regla dura: antes de proponer contenido nuevo, leer este archivo completo y el histórico.**
Nada se sugiere sin chequear contra lo publicado y lo que está en cola.

Última actualización: [fecha]

## Ritmo semanal

Un formato distinto por día, para que no compitan entre sí.

| Día | Formato fijo | Hora | Por qué ese día |
|---|---|---|---|
| | | | |

Excepción por fecha límite: una noticia que pierde valor si espera empuja lo programado un día.
Dos posts el mismo día solo si son de registros muy distintos. Nunca dos del mismo formato.
Comentarios en posts ajenos: continuo, dentro de las 2-3hs del post original, no compiten.

## Cola de publicación

| Fecha | Día | Hora | Categoría | Título | Imagen | Estado |
|---|---|---|---|---|---|---|
| | | | | | | |

Estados: publicado · listo · texto pendiente · tema pendiente.

## Estilo visual

[Bloque base de prompt de imagen, común a todas las piezas. Cambia acá, no en cada prompt.]

## Entradas con texto listo

### [fecha] · [día] [hora] · [CATEGORÍA]

**Por qué ese día:** [criterio]

**Texto:**

> [el post completo, listo para copiar sin editar]

**Prompt de imagen:**

> [el prompt exacto]

**Fuentes (van al primer comentario):** [links]

## Cuarentena

**[Tema] ([fuente], [fecha])**: [por qué es bueno]. Se pisa con [el post del X] por [motivo].
Revivir después del [fecha], reescrito desde el ángulo [nuevo], evitando [la escena que se solapaba].

## Experimentos abiertos

- **Constantes:** [qué no se toca] · **Variable:** [la única que cambia]
- **Qué se compara al corte de 24hs:** [métricas]
````

Reglas de formato que no cambian:
- Link externo siempre al primer comentario, nunca en el cuerpo.
- No recompartir posts propios al día siguiente.

---

## banco-ideas.md

```markdown
# Banco de ideas

## Series en desarrollo
[Ángulo recurrente, con las variantes ya pensadas]

## Hooks sueltos
[Primeras líneas que funcionan y todavía no tienen post. Un buen hook merece post propio, no
ser el remate de otro.]

## Material para posturas
[Tema, ángulo, datos ancla con su link. No el post entero.]

## Notas de uso
- Anclar cada post a algo real y verificado.
- Cerrar sin frase motivacional.
```

---

## historico-performance.md

```markdown
# Histórico de performance

## Cómo cargar esto
- Corte estándar: 24hs después de publicar, siempre el mismo.
- Carruseles y documentos: segundo corte a las 72hs.
- Descontar los comentarios propios. LinkedIn los suma dentro de "Social engagements".
- Anotar también qué se probó distinto respecto del post anterior.

## Datos de contexto
Tamaño de la red: [contactos y seguidores; sin esto las impresiones no se interpretan]
Actualizado: [fecha]

## Registro

### [fecha] · [día y hora] · [título]
Formato: [x] · Categoría: [x] · Imagen: [no / estilo] · Link en 1er comentario: [sí/no]

| Métrica | Valor |
|---|---|
| Impresiones | |
| Members reached | |
| In-network / Out-of-network | |
| Reacciones | |
| Comentarios de terceros | |
| Comentarios propios | |
| Saves | |
| Reposts | |
| Sends | |
| Visitas al perfil | |
| Seguidores ganados | |

Demografía: [top de la vista de analytics]

Lectura: [qué dice este dato, con qué se compara]

## Hipótesis abiertas
[Marcadas como hipótesis hasta tener seis u ocho registros. Cada una con qué la confirmaría o
la refutaría.]

## Pendientes de datos
[Lo que falta medir]
```

---

## Estructura de carpetas

```
posteos/
  2026-08-04-titulo-corto.md     copy publicado, con fecha real de publicación
comentarios/
  2026-08-04-nombre-del-autor.md comentario, link al post original y contexto
carruseles/
  nombre/                         PDF y copy del post que lo acompaña
```

Guardar el copy tal como se publicó, no el borrador. Sirve para no repetirse y para comparar
contra las métricas.
