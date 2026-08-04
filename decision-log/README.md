# decision-log

Un `DECISIONS.md` vivo con las decisiones de desarrollo que **no** se recuperan leyendo el
código.

> A living decision log for the reasoning git cannot give you back.

## Por qué

Git ya te dice qué cambió y cuándo, mejor que cualquier archivo que mantenga una persona.
Lo que git no te dice es por qué el tope es 500 y no 1000, por qué este modelo y no el más
barato, por qué este enfoque después de haber probado el otro.

Ese razonamiento vive en la cabeza de alguien y se va cuando esa persona se va. Seis meses
después otro ve un número sin explicación, asume que era arbitrario, y lo cambia. La caída
que sigue es el costo de no haber escrito un párrafo.

## La regla que lo hace funcionar

**La entrada va en el mismo commit que implementa la decisión.**

No después. Después es una tarea de documentación, las tareas de documentación se
despriorizan, y un log que va atrasado respecto del código es peor que ninguno: describe un
sistema que ya no existe y la gente igual le cree.

## La mitad que se olvida

Leerlo.

Un log que nadie lee es un diario. Los momentos concretos para revisarlo:

- Antes de cambiar un número que parece arbitrario. Normalmente no lo es.
- Antes de proponer un enfoque que parece obvio. Si era obvio y no se hizo, hay una razón, y
  probablemente esté escrita.
- Cuando algo te sorprende. La sorpresa es la señal de que tu modelo del sistema está mal, y
  el log es donde vive la corrección.

Si encontrás una entrada que contradice lo que ibas a hacer, **decilo antes de hacerlo**.
Quizás la decisión venció y hay que actualizar el log; quizás la ibas a revertir a
propósito. Las dos están bien. Hacerlo en silencio no.

## Lo que más se saltea y más ahorra

La decisión de **no** hacer algo.

Sin esa entrada, la próxima persona se pasa un día construyendo lo que vos ya descartaste, y
lo descarta por las mismas razones, con un día menos.

## Instalación

```bash
git clone https://github.com/MR-Axel/skills.git
mkdir -p ~/.claude/skills
cp -r skills/decision-log ~/.claude/skills/
```

Después, en el archivo de instrucciones de tu repo (`CLAUDE.md` o el que uses), sumá una
línea: *las decisiones no obvias se registran en `DECISIONS.md` en el MISMO commit que las
implementa*. Sin eso el skill funciona cuando lo invocás, pero la regla es lo que hace que
pase solo.

## No es un ADR formal

Si ya usás [ADRs](https://adr.github.io/) con un archivo por decisión y un estado
(propuesta, aceptada, reemplazada), seguí con eso: es más riguroso y sirve mejor para
equipos grandes.

Esto es la versión de un archivo, pensada para un equipo chico o para alguien solo, donde la
fricción de crear un archivo nuevo por decisión alcanza para que no se escriba ninguna.

## Datos

`DECISIONS.md` es tuyo y vive en tu repo. El skill no manda nada a ningún lado. Ojo con lo
obvio: si una decisión involucra una credencial, un endpoint privado o un dato de un
usuario, escribí el razonamiento sin el dato. El log se commitea.
