# Calendario editorial

El calendario no es una tabla de horarios. Es la cola de producción y **la fuente de verdad de
todo lo que se propone**. En cuanto alguien publica más de dos veces por semana, sin esta cola
el sistema empieza a canibalizarse: el radar propone temas que se pisan con lo que ya se publicó
o con lo que ya está preparado para dentro de dos días.

## Regla de colisión

**Antes de proponer cualquier post, comentario o idea, leer `calendario.md` completo y el
registro de `historico-performance.md`.**

Un tema colisiona si comparte tesis, escena o dato ancla con algo publicado en los últimos
7 días o con algo que está en cola. Colisionar no es hablar del mismo rubro; es dejar al lector
con la sensación de haber leído esto hace tres días.

Cuando algo colisiona, **no se descarta en silencio y no se propone igual**. Va a cuarentena:

```
### Cuarentena
**[Tema] ([fuente], [fecha])**: [por qué es bueno].
Se pisa con [el post del X] por [motivo concreto].
Revivir después del [fecha], reescrito desde el ángulo [nuevo ángulo],
evitando [la palabra o escena que se solapaba].
```

Un tema en cuarentena con fecha y ángulo nuevo se recupera. Un tema descartado en silencio se
pierde y se vuelve a proponer dentro de dos semanas como si fuera nuevo.

Al presentar hallazgos, decir explícitamente contra qué se chequeó. "Chequeado contra los
últimos 7 días y contra la cola" es una línea que le ahorra a la persona tener que verificarlo.

## Un formato por día

Si se publica todos los días hábiles, cada día debería tener un formato y un registro distintos.
Dos posts del mismo tipo en la misma semana compiten por el mismo lector y por el mismo espacio
en el feed; dos formatos distintos se reparten audiencias distintas.

Ejemplo de ritmo de cinco días, a adaptar según el perfil:

| Día | Formato | Función |
|---|---|---|
| Lunes | Reacción accionable | Algo que se ejecuta esa semana; el lunes se planifica |
| Martes | Pieza larga (carrusel o documento) | Profundidad sobre la red existente |
| Miércoles | Reacción de análisis | Adquisición fuera de la red |
| Jueves | Postura | Conversación |
| Viernes | Historia de construcción | Registro personal |

Quien publica dos o tres veces por semana usa el mismo criterio con menos filas. Lo que no
cambia es el principio: **días distintos, formatos distintos**.

## Excepción por fecha límite

Una noticia con vencimiento real (un precio que cambia, una deadline regulatoria, una ventana
que se cierra) tiene prioridad sobre lo programado y empuja el resto un día. Marcar en la cola
la fecha de vencimiento para que la app la muestre en cuenta regresiva.

Cuidado con la urgencia falsa: que algo sea de hoy no lo hace urgente. Urgente es que pierda
valor si se publica la semana que viene.

**Dos posts el mismo día** solo si son de registros muy distintos, por ejemplo una reacción a la
mañana y un comentario largo en el post de otra persona a la tarde. Nunca dos posts propios del
mismo formato.

## Qué guarda cada entrada

| Campo | Para qué |
|---|---|
| Fecha, día y hora | Cuándo se publica |
| Categoría | Reacción, postura, historia, builder, comentario, cuarentena |
| Título de trabajo | Para reconocerlo de un vistazo |
| Estado | Publicado, listo, texto pendiente, tema pendiente |
| Texto completo | Listo para copiar y pegar, sin editar |
| Prompt de imagen | El prompt exacto, no una descripción de la imagen |
| Fuentes | Los links que van al primer comentario |
| Nota | Por qué va ese día, qué se está probando, qué falta |
| Prioridad y fecha límite | Solo si tiene vencimiento real |
| Métricas | Se cargan cuando pasa al estado publicado |

Un texto guardado a medias no sirve. Si está en la cola como "listo", tiene que poder publicarse
sin volver a escribir nada.

## Prompts de imagen

Si el perfil declara un estilo visual, todo prompt arranca del mismo bloque base y solo cambia
la escena. La consistencia visual hace que a la persona la reconozcan en el feed antes de leer
el nombre, y es de las cosas más baratas de sostener.

Guardar el bloque base en el calendario, no en cada prompt suelto. Cuando cambia el estilo,
cambia en un solo lugar.

Un prompt bien escrito nombra: estilo y época, paleta con códigos de color, la escena concreta,
el sujeto, el texto que va dentro de la imagen si lo hay, y la relación de aspecto. El formato
vertical ocupa más pantalla en el feed móvil.

## La app

`assets/calendario-app.html` es un archivo único, sin dependencias y sin servidor, que muestra la
cola en vista semanal y en lista, con detalle por post, botones de copiar para el texto y el
prompt, y cuenta regresiva para lo que tiene fecha límite.

Los datos viven en un bloque `<script id="datos" type="application/json">` dentro del mismo
archivo, porque un navegador abierto con `file://` no puede leer un JSON externo.

**Para instalarla en la carpeta de trabajo:**

1. Copiar `assets/calendario-app.html` a la carpeta de la persona.
2. Escribir la cola como JSON con el esquema de abajo.
3. Reemplazar el contenido del bloque `<script id="datos">` por ese JSON.
4. Abrir el archivo con doble clic.

**Para actualizarla**, reescribir solo el bloque de datos. Nunca tocar el HTML, el CSS ni el JS:
así la app se puede actualizar desde el repo sin perder los datos, y los datos se pueden
regenerar sin romper la app.

Conviene guardar también el JSON suelto como `calendario-datos.json` al lado de la app. Es más
fácil de editar y de versionar que el bloque embebido.

### Esquema de datos

```json
{
  "marca": "Nombre de la persona",
  "actualizado": "2026-08-05",
  "zonaHoraria": "ART",
  "ritmo": [
    { "dia": "Lunes", "formato": "Reacción", "hora": "8:45am" }
  ],
  "posts": [
    {
      "fecha": "2026-08-10",
      "hora": "8:45am",
      "categoria": "reaccion",
      "titulo": "Título de trabajo",
      "estado": "listo",
      "prioridad": "P1",
      "vence": "2026-08-31",
      "imagen": "Pixel art",
      "nota": "Por qué va ese día y qué se está probando",
      "texto": "El post completo.\n\nCon saltos de párrafo como \\n\\n.",
      "promptImagen": "El prompt exacto para el generador de imágenes",
      "fuentes": ["https://..."],
      "metricas": { "impresiones 24h": 357, "saves": 1 }
    }
  ]
}
```

- `categoria`: `reaccion`, `postura`, `historia`, `builder`, `comentario`, `cuarentena`.
- `estado`: `publicado`, `listo`, `parcial` (texto pendiente), `pendiente` (tema pendiente).
- `dia` se calcula solo desde `fecha`; no hace falta cargarlo.
- Las entradas en cuarentena van sin `fecha`: aparecen agrupadas en la vista de lista.
- Campos opcionales: `prioridad`, `vence`, `imagen`, `nota`, `texto`, `promptImagen`, `fuentes`,
  `metricas`.

Validar el JSON antes de inyectarlo. Un JSON roto deja la app en blanco y el error solo se ve en
la consola del navegador.
