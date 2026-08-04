# Memoria de incidentes

Un archivo, `.claude/memory/incidents.md`, con los bugs que ya te comiste.

El planner lo lee antes de planear y empieza a avisarte de la trampa antes de que caigas.
Es lo que separa un kit que hace siempre lo mismo de uno que aprende de tu repo.

## Por qué no alcanza con "que el modelo lo recuerde"

No lo recuerda. Cada sesión arranca de cero, y los bugs que más duelen no son los que se ven
leyendo el código: son los que dependen de un detalle de tu entorno. Un valor que existe en
producción y no en local. Un paso del build que corre en un lado y no en el otro. Una
librería que se comporta distinto según el runtime.

Ese conocimiento vive en la cabeza de quien lo sufrió, y se pierde cuando esa persona no
está en la conversación. El archivo es donde se deposita.

## Formato

Una entrada por incidente. Lo más nuevo arriba.

```markdown
## <fecha> · <título corto de lo que se rompió>

**Síntoma**: qué se vio. Lo que reportó el usuario o lo que mostró el log, no tu
interpretación.

**Causa raíz**: por qué pasaba de verdad. Si no la encontraste, escribí "no confirmada" y
qué descartaste. Media causa raíz honesta vale más que una completa inventada.

**Por qué no lo vimos antes**: qué gate faltaba. Esta línea es la más útil de todas,
porque es la que se puede arreglar.

**Regla**: qué hacer distinto de ahora en adelante. Concreta y accionable. "Tener cuidado
con el estado" no sirve; "todo handler nuevo se registra en el router en el mismo commit"
sí.
```

## Qué entra y qué no

**Entra** el bug que:

- tardó en encontrarse porque el síntoma apuntaba a otro lado,
- se puede repetir (no fue un typo, fue una trampa del entorno),
- o dejó una regla que alguien nuevo no adivinaría.

**No entra** el bug que se arregló en dos minutos y era obvio. La memoria sirve mientras se
pueda leer entera; si le metés todo, deja de leerse y vuelve a no existir.

Regla práctica: si dentro de seis meses alguien va a volver a caer, escribilo. Si no, dejalo
en el historial de git.

## Un ejemplo real, genérico

```markdown
## 2026-03-12 · Los handlers nuevos daban 404 en producción y andaban en local

**Síntoma**: el endpoint respondía perfecto en el dev server y 404 apenas se deployaba.

**Causa raíz**: el dev server descubre los handlers por convención de archivos; el server
de producción los rutea desde un registro explícito. Un archivo nuevo anda en local sin
registrarse, y en producción no existe.

**Por qué no lo vimos antes**: ningún gate ejercitaba el server de producción. Los tests
corrían la lógica, el build compilaba el bundle, y nadie levantaba el server real.

**Regla**: todo handler nuevo se registra en el router en el MISMO commit, y el gate de
pre push arranca el server de verdad y le pega a una ruta. Un import que rompe el boot no
lo ve ningún test de lógica.
```

## Cómo se mantiene

- **Lo escribe quien lo sufrió**, en el mismo día. Una semana después ya nadie se acuerda
  del síntoma exacto, y el síntoma es la parte que hace que la próxima persona reconozca el
  problema.
- **Se revisa cuando se repite algo.** Si un bug vuelve, la entrada vieja estaba mal escrita
  o la regla no era accionable. Arreglá la entrada, no agregues otra.
- **Se poda.** Una regla que ya es imposible de violar porque el gate la hace cumplir se
  puede borrar. El archivo describe lo que todavía hay que recordar a mano.
