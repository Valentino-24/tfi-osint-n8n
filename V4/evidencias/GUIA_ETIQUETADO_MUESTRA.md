# Cómo etiquetar la muestra de control

Guía para el anotador.

> **Criterio acordado (2026-09-30, tarea 6.1 cerrada).** Cuenta como amenaza lo que
> **describe un ataque o campaña en curso, real y verificable**, aunque se publique
> como reporte. No cuenta el material puramente educativo, de prevención o de
> catálogo. Sin evidencia de un ataque en curso, la categoría es `No relevante`.
>
> Aplicado a los 50 posts, este criterio **no obligó a cambiar ninguna etiqueta**.

Las definiciones de categorías de abajo son las que se usaron. Si un post no encaja
limpio en ninguna, se elige la más cercana y se anota el motivo en `notas`.

## Qué hacés

Abrís `muestra_control_50_2026-09-30_POSTS.csv` en Excel. Por cada fila:

1. Leés `titulo` y `cuerpo`.
2. Elegís **una** categoría de las 10 de abajo.
3. La escribís en `categoria_humana`.
4. Ponés tu nombre en `anotador` y la fecha en `etiquetado_el` (formato `2026-09-30`).

Si el post te dio duda, no lo descartes: etiquetalo igual y anotá el motivo en `notas`. Un post dudoso es información, no basura.

## Las 10 opciones

Nueve son categorías de amenaza. La décima es "esto no es una amenaza".

| Categoría | Cuándo la elegís | Ejemplo |
|---|---|---|
| **No relevante** | No es una amenaza a seguridad informática. Cualquier otra cosa: historia política, empleo, relaciones amorosas, deportes, canciones. | Un post de concerts en Argentina |
| **Phishing** | Engaño para robar datos mediante correo o sitio falso. | "Fake login de X, miren esto" |
| **Robo de Credenciales** | Robo de contraseñas, tarjetas clonadas, sesión secuestrada, salto de 2FA. | "Me clonaron la tarjeta" |
| **Malware** | Software malicioso: troyanos, keyloggers, stealers, ransomware families sin afectación real todavía. | Análisis técnico de un stealer para macOS |
| **Ransomware** | Cifrado de datos y/o Hotline de rescate. | Nota de rescate con nombre de grupo |
| **Vulnerabilidades** | CVE, exploit, fallo de seguridad reportado. | "CVE-2026-94127, heap overflow a RCE" |
| **Filtración de Datos** | Datos que se filtraron: emails, bases, passwords filtradas. | "422 usuarios afectados por esta app falsa" |
| **Infraestructura y Ataques** | Ataques contra redes, servidores, DNS, routers, plantas. | Ataque a un ISP, DNS hijacking |
| **Hacktivismo** | Acción con motivo político/ideológico: defacements, doxxing, filtrado como acción. | Filtración de governmental leaks |
| **Ingenieria Social** | Engaño a personas, no a sistemas: suplantación, vishing, pretexting. | Llamada que se hace pasar por soporte |

> Ojo con los nombres: se escriben **exactamente** como están acá, sin tildes. `Ingenieria Social` va sin tilde, tal como la tiene el sistema. Si escribís `Ingeniería Social` con tilde, el cruce automático no la va a reconocer.

`No relevante` siempre está disponible. Es la respuesta honesta cuando el post no es de seguridad informática, y **usarla no es un error**: hoy el 94 % de la base cae ahí.

## Reglas para decidir

1. **Una sola categoría.** Si un post podría ser dos, elegí la que describe el *impacto principal*. Usá `notas` para registrar la ambigüedad.
2. **Mirá el post, no el subreddit.** Un post de `r/netsec` puede ser perfectamente `No relevante` si habla de otra cosa.
3. **El contexto importa.** Si dice "analicé esta app falsa y hay 422 víctimas", es `Filtración de Datos`. Si dice "publicaron un análisis de esa app falsa", es `Malware`.
4. **Distinguir el ataque del análisis del ataque.** Un análisis técnico de malware sigue siendo `Malware`, no `No relevante`, porque la categoría describe la amenaza de la que habla.
5. **Si es un `[link]` sin cuerpo**, leé el título. Si el título alcanza para decidir, decidí. Si no, poné la categoría más cercana y anotá "título insuficiente" en `notas`.

## Qué NO hacer

- **No usar la predicción del sistema.** No está en tu archivo a propósito. Si llegaste a ver el otro CSV, no lo abras todavía.
- **No descartar posts.** Aunque parezca que no encaja, va etiqueta.
- **No dejar filas vacías.** Si te saltaste una, la única razón válida es que no la pudiste leer, y eso va en `notas`.

## Después

Cuando termines, avisame y yo:
1. Cruzo tus etiquetas contra la predicción del modelo.
2. Calculo la matriz de confusión, precisión, recall y F1 — ponderados por la columna `peso_muestreo` para que los números representen a la base real y no solo a la muestra.
3. Persisto las etiquetas como archivo versionado (tarea 6.4).
