# deploy-qa

QA guiada después de un deploy. Decide qué probar leyendo lo que cambió, en vez de correr
siempre el mismo checklist.

> Guided post deploy QA. Reads the diff, maps it to blast radius, and picks the depth from
> what actually changed.

## El problema que resuelve

Hay dos formas de hacer mal el QA post deploy y las dos son comunes.

La primera es no probar nada porque "era un cambio chico". Un cambio de tres líneas en un
helper con cuarenta consumidores es un cambio de cuarenta consumidores.

La segunda es correr el mismo checklist de cuarenta pasos para todo. Nadie lo hace en serio
después de la tercera vez, y un checklist que se firma sin mirar es peor que ninguno:
produce un registro que dice que se verificó.

Este skill saca la profundidad del alcance real del cambio.

## Lo que más veces resulta ser la respuesta

El paso 0 es confirmar que el build nuevo está realmente sirviéndose.

Un deploy puede reportar éxito y seguir entregando el bundle anterior. Una plataforma puede
mostrar verde mientras el contenedor falló el health check y volvió atrás. Se pierden
cuarenta minutos concluyendo que el fix no funcionó, y el fix nunca había llegado.

Se confirma con el hash del asset, el build id o un endpoint de versión, comparando contra
lo que había antes. Es el chequeo que desarma la mentira.

Aparte: **si tu plataforma no reporta status checks a tu git host, el checkmark verde del
commit no significa nada.** Hay que mirar la plataforma.

## Instalación

```bash
git clone https://github.com/MR-Axel/skills.git
mkdir -p ~/.claude/skills
cp -r skills/deploy-qa ~/.claude/skills/
```

Necesita `.claude/project-profile.md` (la URL desplegada y los comandos), el mismo perfil
que usan los demás skills de desarrollo. Si no lo tenés: [`/project-setup`](../project-setup/).

Uso:

```
/deploy-qa
```

o pasale un commit específico si querés revisar un deploy que ya salió.

## Lo que conviene completar

El skill trae una tabla genérica de path → alcance. Sirve para arrancar, pero **la que la
gente realmente usa es la que nombra tus carpetas**. Escribila una vez, con las rutas de tu
repo, y dejala en el skill o en el archivo de instrucciones del repo.

Las dos reglas que resuelven los casos dudosos:

- **Código compartido no es un cambio chico.** Grepeá los consumidores antes de decidir.
- **La sensibilidad le gana al tamaño.** Plata, auth o borrado de datos van al pase profundo
  sin importar cuántas líneas se movieron. El costo de equivocarse no es proporcional al
  diff.

## Se lleva bien con

[`deploy`](../deploy/), que saca el build; este chequea si sobrevivió el contacto con
producción. Y con [`feature-agents`](../feature-agents/), que cubre las fases anteriores al
push. Cuando algo se rompe, el incidente termina en la memoria de
incidentes que describe ese otro skill, con la línea que más importa: **qué gate lo hubiera
pescado**.

## Datos

No guarda nada y no manda nada a ningún lado. Lee tu git y consulta las URLs de tu propio
deploy.
