# design-system

Establecer un design system donde no hay, y **hacer cumplir** el que ya existe: que
violarlo falle un check en vez de sobrevivir el code review.

> Establish a design system where there is none, and enforce the one that exists so
> violations fail a check instead of surviving review.

## Dónde está el valor

Casi todo lo que se escribe sobre design systems es sobre **autoría**: elegí una escala,
nombrá los tokens, tres capas. Esa parte es una tarde de trabajo y no es la que falla.

Lo que falla es seis meses después, cuando un tercio del código usa los tokens, un tercio usa
valores hardcodeados que casualmente coinciden, y un tercio usa valores que **coincidían**.
Nadie violó el sistema a propósito. Simplemente nunca fue posible violarlo **en voz alta**.

Así que el skill establece rápido y hace cumplir en serio.

## Los cuatro gates

Ninguno necesita una herramienta de regresión visual. Son aserciones de texto sobre tu
propio código, corriendo en la suite que ya tenés.

1. **Prohibir el valor hardcodeado.** La sutileza es que un grep ingenuo lo esquiva un alias
   o un ternario, y un gate que la gente rodea es peor que ninguno.
2. **Gatear el artefacto generado.** Si los tokens compilan a algo, ese archivo se regenera
   en CI y se compara byte a byte. Si no, deriva, y un archivo derivado es peor que ninguno:
   parece autoritativo y está mal.
3. **Asertar el contraste.** Cada par de fondo y texto que el sistema puede producir, como
   test. Un test enumera las combinaciones que nadie diseñó (el acento que elige el usuario,
   el color generado por categoría); un review no puede.
4. **Asertar que los temas estén completos.** Cada token definido en cada tema. Es una
   comparación de sets: cinco líneas, sin opinión, y pesca el caso donde alguien agregó el
   token al tema oscuro y se olvidó del claro. Invisible en desarrollo si solo mirás uno,
   que es lo que hace todo el mundo.

## Las tres trampas que arruinan un sistema recién hecho

**Un token que no puede expresar un estado** fuerza un valor hardcodeado justo cuando el
diseño se pone interesante. Si tu acento es un token, decidí desde el principio cómo se
expresan el fondo teñido al 12%, el borde al 35% y el hover. Lo que **no** funciona es un
helper que compone alpha sobre una variable CSS: en el momento en que corre, la variable es
el string `var(--x)`, no un color. Sale el color opaco (y tu tinte sutil pinta sólido) o se
descarta en silencio. Las dos fallas parecen un error de estilo y son de arquitectura, por
eso duran tanto.

**El contraste por umbral de luminosidad** ("si el fondo es claro, texto oscuro") se
equivoca justo en el medio del rango, que es donde viven los colores de marca. Calculá el
ratio real contra los dos candidatos y quedate con el mejor: cinco líneas, determinista, y
elimina toda la categoría de "en mi monitor se ve bien".

**Un token que existe en un solo tema** es una pantalla que funciona a medias, y la va a
encontrar un usuario antes que vos.

## Instalación

```bash
git clone https://github.com/MR-Axel/skills.git
mkdir -p ~/.claude/skills
cp -r skills/design-system ~/.claude/skills/
```

Usa `.claude/project-profile.md` como el resto de la familia de desarrollo. Si no lo tenés:
[`/project-setup`](../project-setup/).

```
/design-system
```

## Se lleva bien con

[`ux`](../ux/), que es el otro lado. Estos gates protegen **valores**: que el color salga
del token, que el tema esté completo, que el contraste dé. No dicen nada sobre si la
interfaz es buena. Espaciado que respeta la escala puede estar mal igual, y una pantalla
puede ser perfectamente compatible con los tokens y seguir siendo confusa.

Un gate en verde no reemplaza haber mirado la cosa.

## Contenido

- [`references/enforcement.md`](references/enforcement.md) · los cuatro gates en detalle, con
  las sutilezas que hacen que cada uno realmente aguante.
- [`references/patterns.md`](references/patterns.md) · patrones de componentes y los anti
  patrones que producen la mayoría de los bugs de layout y de formularios. Todos están ahí
  porque aparecieron en producción, no porque suenen lindos.

## Datos

No manda nada a ningún lado. Lee y escribe archivos de tu repo.
