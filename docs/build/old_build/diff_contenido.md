# Diferencia de contenido entre el Markdown reconstruido y el PDF aprobado

Fecha: 2026-10-28 17:08

- Markdown: `V4\devoluciones\tesis_v5.md` (sha256 `b1225349198ab4fb…`)
- PDF aprobado: `V4\devoluciones\recuperacion\tesis_v5_aprobado_2026-10-28.pdf` (118 páginas, sha256 `ad6094e65a4da9ca…`)
- Tokens normalizados: PDF 45169, Markdown 44637
- Similitud de secuencia: **0.9875** (umbral 0,97)
- Bloques distintos: 272 (156 en tablas, 116 en texto)
- Tokens afectados: 828 en el PDF, 296 en el Markdown
- Bloques con contenido ausente del otro lado: **0** (más 2 con solo el encabezado repetido de una tabla)

Normalización: minúsculas; todo carácter no ASCII se reemplaza por espacio. Los acentos del PDF salen como U+FFFD por la codificación de las fuentes incrustadas y quedan en la misma posición que los del Markdown. Un token cuenta como presente si aparece en la ventana local (±2500 caracteres) o, con 3 o más letras, como subcadena del texto sin espacios (corte de palabra por justificación: `cread as`). Los tokens de 1 y 2 letras se ignoran: el PDF los produce al partir palabras (`r ne tsec`).

## Bloques con contenido ausente

Ninguno: todas las diferencias son de orden o segmentación; no hay palabras del PDF que falten en el Markdown ni palabras del Markdown que falten en el PDF.

### R1. delete — PDF 5 / Markdown 0 tokens (tabla)

Tocados todos por el **encabezado repetido** de una tabla: Word repite la fila de títulos en cada página y el PDF la contiene varias veces, mientras que el Markdown la tiene una sola vez. No es contenido ausente.

Tokens del PDF ausentes en el Markdown: `rminos`, `listado`

PDF aprobado:

> ad suplantacion de identidad baiting confianza ganada falsa llamada llamada del banco falso empleado falsa policia falso soporte pretexting categor a t rminos listado impersonation pretexto scam call fake support vishing script ayuda de escritorio falsa total 201 el diccionario completo con su extracci n

Markdown:

> ad suplantacion de identidad baiting confianza ganada falsa llamada llamada del banco falso empleado falsa policia falso soporte pretexting

### R2. delete — PDF 13 / Markdown 0 tokens (tabla)

Tocados todos por el **encabezado repetido** de una tabla: Word repite la fila de títulos en cada página y el PDF la contiene varias veces, mientras que el Markdown la tiene una sola vez. No es contenido ausente.

Tokens del PDF ausentes en el Markdown: `bloque`, `elemento`, `origen`

PDF aprobado:

> a no corresponde a publicaciones registradas en la base ni a un incidente verificado por el equipo casos secci n 5 3 caso 2 ransomware a un ilustraci n bloque elemento valor declarado en la v2 v3 origen y respaldo hospital mendocino 05 05 2026 entidad enmascarada generada dem casos secci n 5 3 caso 3 filtraci n de un e commerce nacional 22 06 2026 sco

Markdown:

> no corresponde a publicaciones registradas en la base ni a un incidente verificado por el equipo casos secci n 5 3 caso 2 ransomware a un

## Bloques de 8 tokens o más

| # | tipo | dónde | tokens PDF | tokens MD | contexto en el PDF |
|---|------|-------|-----------:|----------:|--------------------|
| 1 | delete | tabla | 8 | 0 | icaciones marcadas como no relevante 554 182 32 9 sorteadas estrato definici n poblaci n etiquetadas fracci n total 724 352 el estrato 1 se cens ntegro de modo que la pr |
| 2 | replace | tabla | 15 | 1 | s 5 0 69 0 250 3 1 1 filtraci n de datos 4 0 55 0 250 1 0 3 catego r a n puntuaci n media r netsec r malware r devsarg ranso mware 4 0 55 0 250 0 4 0 infraes tructur a y  |
| 3 | replace | tabla | 15 | 1 | ead as con el motor en ejecu ci n 126 9 0 15 7 16 9 97 77 0 subc onjun to n media desv est p50 p95 m ximo 5 min cread as con el motor deteni do 311 371 1 1 557 3 7 020 2  |
| 4 | delete | tabla | 9 | 0 | to 1 censo n 170 referencia no relevante fp 26 26 estrato 2 fn 30 30 clasificador amenaza clasificador no relevante total muestra n 182 referencia amenaza estrato 2 muest |
| 5 | replace | tabla | 11 | 1 | n en el estrato 2 30 de 182 0 165 0 114 0 227 fuente de la incertidum m trica f rmula valor ic 95 exacto alcance bre de la sensibilida d exactitud de categor a 116 de 144 |
| 6 | delete | tabla | 23 | 0 | unid 170 144 26 84 7 78 4 89 8 182 30 16 5 ponder ado 11 4 idio ma com unid ades censo estrato 1 n tp fp precisi n muestr a estrato 2 n omitido s omisi n ades 22 7 el des |
| 7 | replace | tabla | 15 | 6 | e confusi n por categor a referencia clasificador 352 casos refe renc ia clas ifica dor malwa re vulner abilida des phishi ng ranso mware robo de crede nciale s filtrac i |
| 8 | replace | tabla | 22 | 1 | 0 0 2 0 0 0 0 0 rob o de cre den cial es 0 0 0 0 0 1 0 0 0 refe renc ia clas ifica dor malwa re vulner abilida des phishi ng ranso mware robo de crede nciale s filtrac i  |
| 9 | delete | tabla | 17 | 0 | ng ranso mware robo de crede nciale s filtrac i n de datos infrae struct ura y ataqu es hackti vismo no releva nte filtr aci n de dat os 0 0 0 0 0 0 0 0 1 infr aest ruct  |
| 10 | delete | tabla | 12 | 0 | te c 03 malware 1 00 r malwar e 10 06 01 10 ataque clickfix publicaci n categor a puntuaci n comunid ad creada ingerida qu ilustra con captch a falso de cloudflar e caso  |
| 11 | replace | tabla | 14 | 1 | ngesta c 05 vulnerabi lidades 0 50 r netsec 12 10 12 10 rce preautent publicaci n categor a puntuaci n comunid ad creada ingerida qu ilustra icaci n en lg webos una de la |
| 12 | delete | tabla | 12 | 0 | 13 10 falso reclutado r que solicita correo y contrase a de publicaci n categor a puntuaci n comunid ad creada ingerida qu ilustra linkedin patr n de ingenier a social en |
| 13 | delete | tabla | 8 | 0 | pa s 17 d as corte declarado 15 d as evaluados por el motor dimensi n dengra y rivas 2026 este trabajo alcance geogr fico am rica latina y el caribe 5 pa ses una |
| 14 | delete | tabla | 13 | 0 | etivo espec fico evidencia principal estado oe1 recolecci n 724 publicaciones en 17 cumplido con reparos objetivo espec fico evidencia principal estado automatizada con g |
| 15 | delete | tabla | 19 | 0 | ar el motor sobre created utc y excluir de la l nea base la la serie deja de reflejar la operaci n del sistema desaparecen los 5 recomendaci n criterio de verificaci n ca |
| 16 | insert | tabla | 0 | 13 | s fijar la ventana en d as operados y no en d as calendario |
| 17 | delete | tabla | 21 | 0 | 4 860 publicaciones y 22 350 comentarios r devsarg 1 540 y generado las comunidades corresponden al alcance plan b abandonado el bloque elemento valor declarado en la v2  |
| 18 | insert | tabla | 0 | 10 | 20 r derechogenial 1 840 y 8 680 ratios 4 60 7 22 4 71 5 11 |
| 19 | delete | tabla | 13 | 0 | do rendimiento tabla 4 f1 score 0 815 umbral generado el f1 bloque elemento valor declarado en la v2 v3 origen y respaldo 0 800 medido es 0 711 tabla 5 8 sin respaldo ren |
| 20 | delete | tabla | 13 | 0 | cado por el equipo casos secci n 5 3 caso 2 ransomware a un ilustraci n bloque elemento valor declarado en la v2 v3 origen y respaldo hospital mendocino 05 05 2026 entida |
| 21 | delete | tabla | 10 | 0 | bio de objeto registrado como in 07 ventana b5 md secci n 6 fecha hecho destino y evidencia r netsec y r malware 25 30 09 2026 muestra preliminar de 50 publicaciones etiq |

## Bloques menores

| # | tipo | dónde | tokens PDF | tokens MD | contexto en el Markdown |
|---|------|-------|-----------:|----------:|-------------------------|
| 1 | replace | tabla | 2 | 1 | program tico cap tulo 1 1 1 1 2 caracterizacion rate limit md 2 objetivos y criterios de xito automatizaci n estructura |
| 2 | replace | tabla | 2 | 1 | bre el corpus cerrado 19 10 2026 evaluacion muestra control 2026 09 30 consultas archivadas 6 comunicaci n informe acad mi |
| 3 | delete | tabla | 3 | 0 | usi n los estimadores ponderados y los intervalos exactos |
| 4 | delete | tabla | 3 | 0 | descarga el listado p blico de novedades de la comunidad |
| 5 | replace | tabla | 2 | 1 | bscribers integer suscriptores al momento del alta active monitoring boolean interruptor de monitoreo baja l gica created at t |
| 6 | delete | tabla | 7 | 0 | e monitoring boolean interruptor de monitoreo baja l gica |
| 7 | delete | tabla | 7 | 0 | estamptz instante de ingesta base del c lculo de latencia |
| 8 | replace | tabla | 2 | 1 | ntana tabla 5 1 corpus de la ventana b5 por subreddit comunidad suscriptores al alta publicaciones del corpus no relevante |
| 9 | replace | tabla | 2 | 1 | ventana b5 por subreddit comunidad suscriptores al alta publicaciones del corpus no relevante dentro de la comunidad r devsar |
| 10 | replace | tabla | 2 | 1 | ciones del corpus no relevante dentro de la comunidad r devsarg 0 30 09 2026 428 59 12 421 98 36 r netsec 0 30 09 2026 15 |
| 11 | replace | tabla | 2 | 1 | omunidad r devsarg 0 30 09 2026 428 59 12 421 98 36 r netsec 0 30 09 2026 150 20 72 84 56 00 r malware 0 30 09 2026 14 |
| 12 | replace | tabla | 2 | 1 | 12 421 98 36 r netsec 0 30 09 2026 150 20 72 84 56 00 r malware 0 30 09 2026 146 20 17 49 33 56 total 724 100 00 554 76 5 |
| 13 | replace | tabla | 2 | 1 | eto tabla 5 3 clasificaci n tem tica del corpus n 724 categor a n puntuaci n media r netsec r malware r devsarg no re |
| 14 | replace | tabla | 2 | 1 | or a n puntuaci n media r netsec r malware r devsarg no relevante 554 76 52 0 000 84 49 421 malware 79 10 91 0 389 6 73 0 |
| 15 | replace | tabla | 2 | 1 | ware r devsarg no relevante 554 76 52 0 000 84 49 421 malware 79 10 91 0 389 6 73 0 vulnerabilidades 61 8 43 0 320 52 9 |
| 16 | replace | tabla | 3 | 1 | 554 76 52 0 000 84 49 421 malware 79 10 91 0 389 6 73 0 vulnerabilidades 61 8 43 0 320 52 9 0 phishing 12 1 66 0 250 3 8 1 robo |
| 17 | replace | tabla | 2 | 1 | 0 91 0 389 6 73 0 vulnerabilidades 61 8 43 0 320 52 9 0 phishing 12 1 66 0 250 3 8 1 robo de credenciales 5 0 69 0 250 3 1 |
| 18 | replace | tabla | 2 | 1 | 8 43 0 320 52 9 0 phishing 12 1 66 0 250 3 8 1 robo de credenciales 5 0 69 0 250 3 1 1 filtraci n de datos 4 0 55 0 250 1 0 3 |
| 19 | replace | tabla | 3 | 1 | datos 4 0 55 0 250 1 0 3 ransomware 4 0 55 0 250 0 4 0 infraestructura y ataques 3 0 41 0 250 0 2 1 hacktivismo 2 0 28 0 250 1 0 |
| 20 | replace | tabla | 2 | 1 | 0 1 0 3 ransomware 4 0 55 0 250 0 4 0 infraestructura y ataques 3 0 41 0 250 0 2 1 hacktivismo 2 0 28 0 250 1 0 1 total |
| 21 | replace | tabla | 2 | 1 | 250 0 4 0 infraestructura y ataques 3 0 41 0 250 0 2 1 hacktivismo 2 0 28 0 250 1 0 1 total 724 100 00 150 146 428 los por |
| 22 | replace | tabla | 3 | 1 | bla 5 4 latencia extremo a extremo de la ingesta minutos subconjunto n media desv est p50 p95 m ximo 5 min corpus completo d |
| 23 | replace | tabla | 4 | 2 | os subconjunto n media desv est p50 p95 m ximo 5 min corpus completo de la ventana 724 16 483 8 38 407 9 889 9 117 613 1 191 368 |
| 24 | replace | tabla | 2 | 1 | dia desv est p50 p95 m ximo 5 min corpus completo de la ventana 724 16 483 8 38 407 9 889 9 117 613 1 191 368 8 685 94 6 |
| 25 | replace | tabla | 4 | 2 | 724 16 483 8 38 407 9 889 9 117 613 1 191 368 8 685 94 6 creadas dentro de la ventana 01 10 437 400 6 602 4 126 9 1 376 2 7 020 2 3 |
| 26 | replace | tabla | 2 | 1 | 9 889 9 117 613 1 191 368 8 685 94 6 creadas dentro de la ventana 01 10 437 400 6 602 4 126 9 1 376 2 7 020 2 398 91 1 crea |
| 27 | replace | tabla | 2 | 1 | tana 01 10 437 400 6 602 4 126 9 1 376 2 7 020 2 398 91 1 creadas desde el 02 10 409 390 9 521 9 126 1 1 392 2 3 031 2 374 91 |
| 28 | replace | tabla | 2 | 1 | e el 02 10 409 390 9 521 9 126 1 1 392 2 3 031 2 374 91 4 creadas con el motor en ejecuci n 126 9 0 15 7 16 9 97 77 0 cread |
| 29 | replace | tabla | 2 | 1 | 9 126 1 1 392 2 3 031 2 374 91 4 creadas con el motor en ejecuci n 126 9 0 15 7 16 9 97 77 0 creadas con el motor detenido |
| 30 | replace | tabla | 2 | 1 | ejecuci n 126 9 0 15 7 16 9 97 77 0 creadas con el motor detenido 311 371 1 1 557 3 7 020 2 301 96 8 la lectura de esta tab |
| 31 | replace | tabla | 2 | 1 | tabla 5 6 evaluaciones del motor por categor a categor a evaluaciones observados disparos l nea base media umbral medio vulne |
| 32 | replace | tabla | 2 | 1 | iones observados disparos l nea base media umbral medio vulnerabilidades 15 59 2 2 95 6 87 malware 15 79 1 4 00 8 33 filtraci n |
| 33 | replace | tabla | 2 | 1 | tos 15 4 0 0 19 3 00 phishing 15 11 1 0 57 3 00 robo de credenciales 15 5 0 0 25 3 00 hacktivismo 14 2 0 0 11 3 00 ransomwar |
| 34 | replace | tabla | 2 | 1 | 15 11 1 0 57 3 00 robo de credenciales 15 5 0 0 25 3 00 hacktivismo 14 2 0 0 11 3 00 ransomware 14 4 1 0 24 3 00 infraestru |
| 35 | replace | tabla | 2 | 1 | denciales 15 5 0 0 25 3 00 hacktivismo 14 2 0 0 11 3 00 ransomware 14 4 1 0 24 3 00 infraestructura y ataques 9 3 1 0 27 3 0 |
| 36 | replace | tabla | 2 | 1 | acktivismo 14 2 0 0 11 3 00 ransomware 14 4 1 0 24 3 00 infraestructura y ataques 9 3 1 0 27 3 00 total 112 167 6 el n mero de |
| 37 | insert | tabla | 0 | 3 | vante fp 26 26 estrato 2 muestra n 182 referencia amenaza fn 30 30 estrato 2 muestra n 182 referencia no relevante tn 152 15 |
| 38 | replace | tabla | 2 | 1 | p 144 170 0 847 0 784 0 898 censada sin error de muestreo sensibilidad recall tp tp w k 144 144 3 044 30 0 612 0 534 0 695 pondera |
| 39 | replace | tabla | 2 | 1 | edia arm nica de p y s 0 711 0 635 0 783 derivada intervalo conservador tasa de falsos descubrimientos fp tp fp 26 170 0 153 comp |
| 40 | replace | tabla | 2 | 1 | 0 635 0 783 derivada intervalo conservador tasa de falsos descubrimientos fp tp fp 26 170 0 153 complemento de la precisi n omisi n |
| 41 | replace | tabla | 2 | 1 | ador tasa de falsos descubrimientos fp tp fp 26 170 0 153 complemento de la precisi n omisi n en el estrato 2 30 de 182 0 165 0 |
| 42 | replace | tabla | 2 | 1 | 0 de 182 0 165 0 114 0 227 fuente de la incertidumbre de la sensibilidad exactitud de categor a 116 de 144 amenazas detectadas 0 8 |
| 43 | replace | tabla | 4 | 2 | o del clasificador por comunidad validaci n v5 352 casos comunidad predicciones positivas censo tp fp precisi n muestra del estrato negativ |
| 44 | replace | tabla | 2 | 1 | ecisi n muestra del estrato negativo omitidas omisi n r netsec 66 60 6 90 9 29 15 51 7 r malware 97 81 16 83 5 18 13 72 |
| 45 | replace | tabla | 2 | 1 | o omitidas omisi n r netsec 66 60 6 90 9 29 15 51 7 r malware 97 81 16 83 5 18 13 72 2 r devsarg 7 3 4 42 9 135 2 1 5 |
| 46 | replace | tabla | 2 | 1 | 6 90 9 29 15 51 7 r malware 97 81 16 83 5 18 13 72 2 r devsarg 7 3 4 42 9 135 2 1 5 dos lecturas se imponen primera el c |
| 47 | replace | tabla | 5 | 2 | 5 9 b desempe o por idioma espa ol ingl s validaci n v5 idioma comunidades censo estrato 1 n tp fp precisi n muestra estrato 2 n omiti |
| 48 | replace | tabla | 2 | 1 | v5 idioma comunidades censo estrato 1 n tp fp precisi n muestra estrato 2 n omitidos omisi n espa ol rioplatense r devs |
| 49 | replace | tabla | 2 | 1 | dades censo estrato 1 n tp fp precisi n muestra estrato 2 n omitidos omisi n espa ol rioplatense r devsarg 7 3 4 42 9 135 2 |
| 50 | replace | tabla | 3 | 1 | precisi n muestra estrato 2 n omitidos omisi n espa ol rioplatense r devsarg 7 3 4 42 9 135 2 1 5 ingl s r netsec r malware |
| 51 | replace | tabla | 3 | 1 | stra estrato 2 n omitidos omisi n espa ol rioplatense r devsarg 7 3 4 42 9 135 2 1 5 ingl s r netsec r malware 163 141 22 |
| 52 | replace | tabla | 2 | 1 | pa ol rioplatense r devsarg 7 3 4 42 9 135 2 1 5 ingl s r netsec r malware 163 141 22 86 5 47 28 59 6 total las tres comun |
| 53 | replace | tabla | 3 | 1 | platense r devsarg 7 3 4 42 9 135 2 1 5 ingl s r netsec r malware 163 141 22 86 5 47 28 59 6 total las tres comunidades 170 |
| 54 | replace | tabla | 2 | 1 | etsec r malware 163 141 22 86 5 47 28 59 6 total las tres comunidades 170 144 26 84 7 78 4 89 8 182 30 16 5 ponderado 11 4 22 7 |
| 55 | replace | tabla | 2 | 1 | las tres comunidades 170 144 26 84 7 78 4 89 8 182 30 16 5 ponderado 11 4 22 7 el desglose por idioma confirma lo observado en |
| 56 | replace | tabla | 5 | 2 | icador malware vulnerabilidades phishing ransomware robo de credenciales filtraci n de datos infraestructura y ataques hacktivismo no relevan |
| 57 | replace | tabla | 3 | 1 | hishing ransomware robo de credenciales filtraci n de datos infraestructura y ataques hacktivismo no relevante malware 59 7 5 2 2 0 |
| 58 | replace | tabla | 4 | 2 | robo de credenciales filtraci n de datos infraestructura y ataques hacktivismo no relevante malware 59 7 5 2 2 0 1 0 14 vulnerabilid |
| 59 | replace | tabla | 5 | 2 | iltraci n de datos infraestructura y ataques hacktivismo no relevante malware 59 7 5 2 2 0 1 0 14 vulnerabilidades 2 49 2 0 1 1 0 0 12 |
| 60 | replace | tabla | 5 | 1 | hacktivismo no relevante malware 59 7 5 2 2 0 1 0 14 vulnerabilidades 2 49 2 0 1 1 0 0 12 phishing 1 0 5 0 0 0 0 0 3 ransomwa |
| 61 | replace | tabla | 2 | 1 | 9 7 5 2 2 0 1 0 14 vulnerabilidades 2 49 2 0 1 1 0 0 12 phishing 1 0 5 0 0 0 0 0 3 ransomware 0 0 0 2 0 0 0 0 0 robo de |
| 62 | replace | tabla | 4 | 1 | ilidades 2 49 2 0 1 1 0 0 12 phishing 1 0 5 0 0 0 0 0 3 ransomware 0 0 0 2 0 0 0 0 0 robo de credenciales 0 0 0 0 0 1 0 0 0 |
| 63 | replace | tabla | 2 | 1 | phishing 1 0 5 0 0 0 0 0 3 ransomware 0 0 0 2 0 0 0 0 0 robo de credenciales 0 0 0 0 0 1 0 0 0 filtraci n de datos 0 0 |
| 64 | replace | tabla | 4 | 1 | 1 0 5 0 0 0 0 0 3 ransomware 0 0 0 2 0 0 0 0 0 robo de credenciales 0 0 0 0 0 1 0 0 0 filtraci n de datos 0 0 0 0 0 0 0 0 1 |
| 65 | replace | tabla | 4 | 1 | 0 0 0 0 0 1 0 0 0 filtraci n de datos 0 0 0 0 0 0 0 0 1 infraestructura y ataques 1 0 0 0 1 0 1 1 0 no relevante 16 5 0 0 1 2 1 1 |
| 66 | replace | tabla | 3 | 1 | filtraci n de datos 0 0 0 0 0 0 0 0 1 infraestructura y ataques 1 0 0 0 1 0 1 1 0 no relevante 16 5 0 0 1 2 1 1 152 la |
| 67 | replace | tabla | 3 | 1 | 0 0 0 1 infraestructura y ataques 1 0 0 0 1 0 1 1 0 no relevante 16 5 0 0 1 2 1 1 152 la diagonal concentra 268 de los 352 |
| 68 | replace | tabla | 2 | 1 | malware 0 50 suplantaci n de identidad en redes sociales r derechogenial 0 25 el diccionario marca material de defensa y contenido f |
| 69 | replace | tabla | 4 | 2 | i n por comunidad publicaciones con al menos una entidad subreddit publicaciones con entidad cve ip correo dominio producto r devsarg 42 |
| 70 | replace | tabla | 2 | 1 | subreddit publicaciones con entidad cve ip correo dominio producto r devsarg 428 162 0 1 4 27 150 r netsec 150 51 27 1 2 |
| 71 | replace | tabla | 2 | 1 | licaciones con entidad cve ip correo dominio producto r devsarg 428 162 0 1 4 27 150 r netsec 150 51 27 1 2 9 23 r malw |
| 72 | replace | tabla | 2 | 1 | reo dominio producto r devsarg 428 162 0 1 4 27 150 r netsec 150 51 27 1 2 9 23 r malware 146 73 5 2 3 41 47 c mo r |
| 73 | replace | tabla | 2 | 1 | sarg 428 162 0 1 4 27 150 r netsec 150 51 27 1 2 9 23 r malware 146 73 5 2 3 41 47 c mo reconoce el sistema cada familia |
| 74 | replace | tabla | 2 | 1 | entativos del corpus b5 publicaci n categor a puntuaci n comunidad creada ingerida qu ilustra c 01 malware 1 00 r malware |
| 75 | replace | tabla | 2 | 1 | omunidad creada ingerida qu ilustra c 01 malware 1 00 r malware 14 10 14 10 advertencia sobre un repositorio falso que dist |
| 76 | replace | tabla | 2 | 1 | rida qu ilustra c 01 malware 1 00 r malware 14 10 14 10 advertencia sobre un repositorio falso que distribuye un infostealer de |
| 77 | replace | tabla | 2 | 1 | 01 malware 1 00 r malware 14 10 14 10 advertencia sobre un repositorio falso que distribuye un infostealer detecci n de m xima con |
| 78 | replace | tabla | 2 | 1 | ware 14 10 14 10 advertencia sobre un repositorio falso que distribuye un infostealer detecci n de m xima confianza sobre un incid |
| 79 | replace | tabla | 2 | 1 | 10 advertencia sobre un repositorio falso que distribuye un infostealer detecci n de m xima confianza sobre un incidente en curso |
| 80 | replace | tabla | 2 | 1 | confianza sobre un incidente en curso c 02 malware 1 00 r malware 03 10 04 10 cargador de mando y control preinstalado en pro |
| 81 | replace | tabla | 2 | 1 | ware 1 00 r malware 03 10 04 10 cargador de mando y control preinstalado en proyectores android creada durante el hueco operativo y |
| 82 | replace | tabla | 2 | 1 | are 03 10 04 10 cargador de mando y control preinstalado en proyectores android creada durante el hueco operativo y recuperada en e |
| 83 | replace | tabla | 2 | 1 | en proyectores android creada durante el hueco operativo y recuperada en el ciclo siguiente c 03 malware 1 00 r malware 10 06 0 |
| 84 | replace | tabla | 2 | 1 | vo y recuperada en el ciclo siguiente c 03 malware 1 00 r malware 10 06 01 10 ataque clickfix con captcha falso de cloudflare |
| 85 | replace | tabla | 2 | 1 | c 03 malware 1 00 r malware 10 06 01 10 ataque clickfix con captcha falso de cloudflare caso de arrastre inicial 113 d as entre |
| 86 | replace | tabla | 2 | 1 | r malware 10 06 01 10 ataque clickfix con captcha falso de cloudflare caso de arrastre inicial 113 d as entre creaci n e ingesta |
| 87 | replace | tabla | 2 | 1 | e arrastre inicial 113 d as entre creaci n e ingesta c 04 vulnerabilidades 0 50 r netsec 09 10 09 10 cadena de rce preautenticaci n en |
| 88 | replace | tabla | 2 | 1 | 04 vulnerabilidades 0 50 r netsec 09 10 09 10 cadena de rce preautenticaci n en papercut el hilo remite a los avisos wt 2026 0141 0144 |
| 89 | replace | tabla | 2 | 1 | y cve 2026 81578 misma jornada de creaci n e ingesta c 05 vulnerabilidades 0 50 r netsec 12 10 12 10 rce preautenticaci n en lg webos |
| 90 | replace | tabla | 2 | 1 | 10 12 10 rce preautenticaci n en lg webos una de las cuatro publicaciones que provocaron el nico disparo del motor sobre actividad de |
| 91 | replace | tabla | 2 | 1 | tenticaci n en lg webos una de las cuatro publicaciones que provocaron el nico disparo del motor sobre actividad de las comunidade |
| 92 | replace | tabla | 2 | 1 | provocaron el nico disparo del motor sobre actividad de las comunidades c 06 hacktivismo 0 25 r devsarg 12 10 12 10 ataque al sit |
| 93 | replace | tabla | 2 | 1 | disparo del motor sobre actividad de las comunidades c 06 hacktivismo 0 25 r devsarg 12 10 12 10 ataque al sitio oficial de una f |
| 94 | replace | tabla | 2 | 1 | obre actividad de las comunidades c 06 hacktivismo 0 25 r devsarg 12 10 12 10 ataque al sitio oficial de una fundaci n local |
| 95 | replace | tabla | 2 | 1 | 2 10 ataque al sitio oficial de una fundaci n local caso de relevancia local que un diccionario solo en ingl s no habr a detectado |
| 96 | replace | tabla | 2 | 1 | cial de una fundaci n local caso de relevancia local que un diccionario solo en ingl s no habr a detectado c 07 phishing 0 25 r d |
| 97 | replace | tabla | 2 | 1 | elevancia local que un diccionario solo en ingl s no habr a detectado c 07 phishing 0 25 r devsarg 13 10 13 10 falso reclutador |
| 98 | replace | tabla | 2 | 1 | o solo en ingl s no habr a detectado c 07 phishing 0 25 r devsarg 13 10 13 10 falso reclutador que solicita correo y contrase |
| 99 | replace | tabla | 2 | 1 | detectado c 07 phishing 0 25 r devsarg 13 10 13 10 falso reclutador que solicita correo y contrase a de linkedin patr n de inge |
| 100 | replace | tabla | 2 | 1 | kedin patr n de ingenier a social en espa ol c 08 robo de credenciales 0 25 r devsarg 15 10 15 10 falso positivo discusi n sobre i |
| 101 | replace | tabla | 2 | 1 | nier a social en espa ol c 08 robo de credenciales 0 25 r devsarg 15 10 15 10 falso positivo discusi n sobre ingenier a inver |
| 102 | replace | tabla | 2 | 1 | 15 10 falso positivo discusi n sobre ingenier a inversa de videojuegos sin amenaza c 09 filtraci n de datos 0 25 r devsarg 10 10 |
| 103 | replace | tabla | 2 | 1 | e videojuegos sin amenaza c 09 filtraci n de datos 0 25 r devsarg 10 10 10 10 falso positivo consulta sobre c mo almacenar da |
| 104 | replace | tabla | 2 | 1 | 25 r devsarg 10 10 10 10 falso positivo consulta sobre c mo almacenar datos personales en una aplicaci n c 10 infraestructura y |
| 105 | replace | tabla | 2 | 1 | 10 10 10 falso positivo consulta sobre c mo almacenar datos personales en una aplicaci n c 10 infraestructura y ataques 0 25 r d |
| 106 | replace | tabla | 2 | 1 | re c mo almacenar datos personales en una aplicaci n c 10 infraestructura y ataques 0 25 r devsarg 26 09 01 10 falso positivo reflexi |
| 107 | replace | tabla | 2 | 1 | s en una aplicaci n c 10 infraestructura y ataques 0 25 r devsarg 26 09 01 10 falso positivo reflexi n sobre aprendizaje e in |
| 108 | replace | tabla | 2 | 1 | s 0 25 r devsarg 26 09 01 10 falso positivo reflexi n sobre aprendizaje e inteligencia artificial sin relaci n con ataques t rmi |
| 109 | replace | tabla | 2 | 1 | rg 26 09 01 10 falso positivo reflexi n sobre aprendizaje e inteligencia artificial sin relaci n con ataques t rminos que coincid |
| 110 | insert | tabla | 0 | 4 | automatizada con gesti n expl cita de restricciones de tasa 724 publicaciones en 17 jornadas de operaci n parcial 19 0 del per odo caracterizac |
| 111 | replace | tabla | 2 | 1 | de operaci n parcial 19 0 del per odo caracterizacion rate limit md interrupci n de 44 h declarada con causa apagado del equ |
| 112 | insert | tabla | 0 | 3 | i n de 44 h declarada con causa apagado del equipo el 03 10 cumplido con reparos oe2 flujos robustos en n8n con idempotencia y recuperaci |
| 113 | delete | tabla | 6 | 0 | ablas 5 5 5 6 y 5 4 1 implementado eficacia no demostrada |
| 114 | replace | texto | 2 | 1 | v4 m 21 alertas estado default pendiente era enviada una inserci n sin estado expl cito quedaba registrada como enviada aun |
| 115 | replace | texto | 2 | 1 | idempotencia del nodo de an lisis a la base reejecutar el motor no duplica evaluaciones la latencia publicaci n ingest |
| 116 | replace | texto | 2 | 1 | ubreddit id varchar 50 not null references subreddits id on delete restrict title text not null selftext text url text |
| 117 | replace | texto | 2 | 1 | text text url text author hash char 64 not null usuario seudonimizado hmac sha 256 score integer default 0 num comments integ |
| 118 | replace | texto | 2 | 1 | default 0 created utc timestamptz not null fecha real de publicaci n en reddit nlp category varchar 100 salida del clasificad |
| 119 | replace | texto | 2 | 1 | publicaci n en reddit nlp category varchar 100 salida del clasificador por diccionario nlp score real check nlp score between 0 a |
| 120 | replace | texto | 2 | 1 | 0 and 1 n 06 puntuaci n 0 1 entities jsonb n 06 entidades extra das oe4 nlp processed boolean default false ingested at |
| 121 | replace | texto | 2 | 1 | ingested at timestamptz default current timestamp cu ndo lo ingiri el sistema latencia 3 comentarios asociados create ta |
| 122 | replace | texto | 2 | 1 | post id varchar 50 not null references posts id on delete cascade body text not null author hash char 64 not null score |
| 123 | replace | texto | 2 | 1 | alizada ventana fin timestamptz not null fin de la ventana analizada categoria varchar 100 not null n observado integer not n |
| 124 | replace | texto | 2 | 1 | en la ventana base media real not null promedio hist rico de la categor a umbral real not null umbral disparado justifi |
| 125 | replace | texto | 2 | 1 | rico de la categor a umbral real not null umbral disparado justificado en 4 5 disparo boolean not null default false created a |
| 126 | replace | texto | 2 | 1 | p m 21 una evaluaci n por categor a ventana reejecutar el motor no duplica constraint anomalias categoria ventana uniq uni |
| 127 | replace | texto | 2 | 1 | onstraint anomalias categoria ventana uniq unique categoria ventana inicio 5 alertas registradas n 06 m 21 create table |
| 128 | replace | texto | 2 | 1 | ate index if not exists idx posts nlp category on posts nlp category create index if not exists idx posts ingested at on posts |
| 129 | replace | texto | 2 | 1 | index if not exists idx posts ingested at on posts ingested at create index if not exists idx comments post id on commen |
| 130 | replace | tabla | 2 | 1 | inventario de nodos y responsabilidades nodo tipo flujo responsabilidad 1 schedule ingesta scheduletrigger ingesta dispara el c |
| 131 | replace | tabla | 2 | 1 | s nodo tipo flujo responsabilidad 1 schedule ingesta scheduletrigger ingesta dispara el ciclo cada 15 minutos 2 prepare subred |
| 132 | replace | tabla | 2 | 1 | sta alta y actualizaci n de comunidades 4 loop over items splitinbatches ingesta itera comunidades lote de tama o 1 5 espera rate |
| 133 | delete | tabla | 5 | 0 | al 12 upsert posts postgres ingesta insert on conflict do |
| 134 | replace | tabla | 2 | 1 | t on conflict do update idempotente 13 schedule anomalias scheduletrigger an lisis dispara el an lisis a las 12 05 14 query daily c |
| 135 | replace | texto | 2 | 1 | w error falta la variable de entorno osint hmac key seteala antes de arrancar n8n ver guia ejecucion md const out for c |
| 136 | replace | texto | 2 | 1 | all if item json skip out push item continue centinela de 429 pasa intacto out push json item json author hash cry |
| 137 | replace | texto | 2 | 1 | author hash crypto createhmac sha256 key update string item json author digest hex created utc iso new date item json crea |
| 138 | replace | texto | 2 | 1 | hex created utc iso new date item json created utc 0 1000 toisostring delete out out length 1 json author return out |
| 139 | replace | texto | 2 | 1 | sificador por diccionario bilingue es en 9 categorias texto normalizado sin acentos match terminos de una palabra por token exact |
| 140 | replace | texto | 2 | 1 | icciones que el diccionario respeta si se rompen el termino nunca encontraria el texto sin tildes la normalizacion nfd las |
| 141 | replace | texto | 2 | 1 | sin tildes la normalizacion nfd las saca del texto no del termino bufer nunca encontraria el texto sin guiones el tokenizad |
| 142 | replace | texto | 2 | 1 | y la cadena con guion nunca aparece como token escribi zero day con las formas conjugadas reales filtraron no matchea con |
| 143 | replace | texto | 2 | 1 | con las formas conjugadas reales filtraron no matchea con filtrar se sacaron los cuasisinonimos demasiado genericos mp cuen |
| 144 | replace | texto | 2 | 1 | ansferencia banco filtrar cangrejo pescar actualizacion por falsos positivos 2026 09 30 se saco dni de filtraci n de datos p |
| 145 | replace | texto | 2 | 1 | re dar de baja apoderado de jubilacion anses que es tramite administrativo y no una filtracion con min hits 2 el falso positivo no se |
| 146 | replace | texto | 2 | 1 | ion con min hits 2 el falso positivo no se notaba porque el post tenia un solo hit al bajar el umbral a 1 se hizo visible u |
| 147 | replace | texto | 2 | 1 | ar el umbral a 1 se hizo visible un termino que matchea con paperwork es demasiado generico f rmula de puntuaci n 4 4 ahora sat |
| 148 | replace | texto | 2 | 1 | s por qu el cambio antes era score hits c keywords c y el denominador depende del tama o del diccionario al ampliarlo de 5 a 9 c |
| 149 | replace | texto | 2 | 1 | diccionario al ampliarlo de 5 a 9 categor as y de 10 a 22 t rminos cada una el mismo post con los mismos 2 hits pasaba de 0 2 |
| 150 | replace | texto | 2 | 1 | st con los mismos 2 hits pasaba de 0 22 a 0 07 la escala se comprime y nlp score deja de ser comparable entre corridas y entre |
| 151 | replace | texto | 2 | 1 | arable entre corridas y entre categor as saturation fija la escala 2 hits 0 5 3 0 75 4 1 0 independiente del tama o del dicc |
| 152 | replace | texto | 2 | 1 | hits bajado de 2 a 1 2026 09 30 evaluacion de la muestra de control de 50 posts con min hits 2 el clasificador descartaba ame |
| 153 | replace | texto | 2 | 1 | min hits 2 el clasificador descartaba amenazas obvias fake interpol investigation emails are dropping ransomware on small busi |
| 154 | replace | texto | 2 | 1 | re dropping ransomware on small businesses tiene la palabra ransomware en el titulo el termino existe en el diccionario y matchea |
| 155 | replace | texto | 2 | 1 | evos son terminos demasiado genericos del diccionario no un efecto del umbral dni matcheaba con un post sobre dar de baja un |
| 156 | replace | texto | 2 | 1 | dni matcheaba con un post sobre dar de baja un apoderado de jubilacion y se saco en el mismo commit ver filtraci n de datos min h |
| 157 | replace | texto | 2 | 1 | o commit ver filtraci n de datos min hits 1 tambien absorbe el ruido de fondo que antes salia suplantacion de identidad m |
| 158 | replace | texto | 2 | 1 | egaron esos terminos definirlos sin conocimiento tecnico de ciberseguridad meteria el mismo error conceptual adentro del diccionario |
| 159 | replace | texto | 2 | 1 | o error conceptual adentro del diccionario documentado como limitacion abierta en v4 evidencias evaluacion muestra control 2026 0 |
| 160 | replace | texto | 2 | 1 | nst dict phishing phishing phisher smishing vishing spear phishing correo fraudulento correo suplantado remitente falso enlace |
| 161 | replace | texto | 2 | 1 | ishing correo fraudulento correo suplantado remitente falso enlace fraudulento enlace sospechoso pagina falsa sitio falso port |
| 162 | replace | texto | 2 | 1 | lace fraudulento enlace sospechoso pagina falsa sitio falso portal falso ingreso falso verificar identidad verificacion de ide |
| 163 | replace | texto | 2 | 1 | tal falso ingreso falso verificar identidad verificacion de identidad captura de datos suplantacion de correo business email comp |
| 164 | replace | texto | 2 | 1 | idad captura de datos suplantacion de correo business email compromise fake login credential harvest harvesting robo de credenci |
| 165 | replace | texto | 2 | 1 | robo de credenciales clonacion de tarjeta tarjeta clonada clonar robo de contrasena robaron mi contrasena cambio de contrase |
| 166 | replace | texto | 2 | 1 | a clonar robo de contrasena robaron mi contrasena cambio de contrasena cambiar mi contrasena acceso no autorizado acceso remoto to |
| 167 | replace | texto | 2 | 1 | na cambiar mi contrasena acceso no autorizado acceso remoto tomaron control de la cuenta tomo control de mi cuenta sesion robad |
| 168 | replace | texto | 2 | 1 | robada robo de token segundo factor factor de autenticacion credential stuffing account takeover session hijacking session hijack |
| 169 | replace | texto | 2 | 1 | s mfa fatigue sim swap sim swapping otp bypass push bombing adversary in the middle malware malware virus troyano troyano gusan |
| 170 | replace | texto | 2 | 1 | ol c2 server rat packed obfuscated ofuscado payload reverse shell bind shell webshell ransomware ransomware nota de rescate |
| 171 | replace | texto | 2 | 1 | rescate bloquearon mis archivos mis archivos estan cifrados secuestro de datos extorsion wannacry lockbit revil blackcat locker d |
| 172 | replace | texto | 2 | 1 | ar patch tuesday actualizacion de seguridad backdoor puerta trasera zero day prueba de concepto proof of concept inyeccion sql |
| 173 | replace | texto | 2 | 1 | eccion sql sql injection xss rce ejecucion remota de codigo escalamiento de privilegios buffer overflow desbordamiento de buffer byp |
| 174 | replace | texto | 2 | 1 | nto de privilegios buffer overflow desbordamiento de buffer bypass de autenticacion authentication bypass kerberoasting movimi |
| 175 | replace | texto | 2 | 1 | bypass de autenticacion authentication bypass kerberoasting movimiento lateral lateral movement privilege escalation nvd cisa zero |
| 176 | replace | texto | 2 | 1 | ran fuga de datos fuga de informacion base filtrada base de datos expuesta bases expuestas base expuesta datos personales ven |
| 177 | replace | texto | 2 | 1 | tos expuesta bases expuestas base expuesta datos personales venta de datos venden datos vazamiento exfiltracion exfiltrated l |
| 178 | replace | texto | 2 | 1 | iltrated leak leaked leaks breach breached exposed database exposed credentials credentials dump combo list dark web pastebin d |
| 179 | replace | texto | 2 | 1 | se exposed credentials credentials dump combo list dark web pastebin data dump breach notification infraestructura y ataques b |
| 180 | replace | texto | 2 | 1 | denial of service caida de servicio sitio caido tiraron el sitio tiraron abajo el sitio ataque de red amplificacion reflecti |
| 181 | replace | texto | 2 | 1 | el sitio tiraron abajo el sitio ataque de red amplificacion reflection attack volumetric ip flood takedown cayeron los servidores |
| 182 | replace | texto | 2 | 1 | reflection attack volumetric ip flood takedown cayeron los servidores caida de servidores hacktivismo hacktivismo hacktivista h |
| 183 | replace | texto | 2 | 1 | ores hacktivismo hacktivismo hacktivista hackeo hackearon hackear deface defacement defaced dox doxeado doxing anonymous filt |
| 184 | replace | texto | 2 | 1 | onymous filtracion publicada publicacion de datos filtrados protesta hacker hactivist ingenieria social ingenieria social soci |
| 185 | replace | texto | 2 | 1 | st ingenieria social ingenieria social social engineering mecanismo de engano se hacen pasar suplantar identidad suplantacion d |
| 186 | replace | texto | 2 | 1 | o de engano se hacen pasar suplantar identidad suplantacion de identidad baiting confianza ganada falsa llamada llamada de |
| 187 | replace | texto | 2 | 1 | de identidad baiting confianza ganada falsa llamada llamada del banco falso empleado falsa policia falso soporte pretexting |
| 188 | replace | texto | 2 | 1 | xting impersonation pretexto scam call fake support vishing script ayuda de escritorio falsa const min hits 1 const satu |
| 189 | replace | texto | 2 | 1 | saturation 4 hits a partir de los cuales el score vale 1 0 escala fija ver cabecera const norm s string s tolowercase norma |
| 190 | replace | texto | 2 | 1 | cabecera const norm s string s tolowercase normalize nfd replace u0300 u036f g const out for const item of input all i |
| 191 | replace | texto | 2 | 1 | all if item json skip out push item continue centinela de 429 no se clasifica const text norm item json title item json |
| 192 | replace | texto | 2 | 1 | f dict cat const k kw includes text includes kw 1 0 words has kw 1 0 hits k if hits besthits besthits hits best |
| 193 | replace | texto | 2 | 1 | extracci n de entidades oe4 n 06 cve emails ips dominios y productos const products whatsapp telegram mercado pago windows lin |
| 194 | replace | texto | 2 | 1 | tos const products whatsapp telegram mercado pago windows linux android ios chrome firefox bitcoin usdt afi p banco nacion |
| 195 | replace | texto | 2 | 1 | ado libre const norm s string s tolowercase normalize nfd replace u0300 u036f g const uniq a array from new set a const o |
| 196 | replace | texto | 2 | 1 | all if item json skip out push item continue centinela de 429 sin entidades const raw item json title item json selftext |
| 197 | replace | texto | 2 | 1 | t entities cves uniq low match bcve d 4 d 4 7 b g map x x touppercase slice 0 20 emails uniq raw match b w w w b g slice 0 20 |
| 198 | replace | texto | 2 | 1 | net io gov edu b g filter d d startswith reddit com slice 0 20 products uniq products filter p low includes p slice 0 20 |
| 199 | replace | texto | 2 | 1 | or de anomal as 4 5 ventana diaria base media diaria de los 10 d as previos umbral max cuantil 95 de poisson 1 m nimo ab |
| 200 | replace | texto | 2 | 1 | f rota satura en 1 l asi que para l 1 05 nunca alcanza 0 95 el while de busqueda del umbral corre hasta el tope de 500 y |
| 201 | replace | texto | 2 | 1 | rdia anti centinela in 08 el item de error que genera parse reddit posts cuando reddit responde 429 viaja por toda la cadena |
| 202 | replace | texto | 2 | 1 | ddit responde 429 viaja por toda la cadena para que el loop no se corte pero no debe terminar en la tabla el sub que fall |
| 203 | replace | texto | 2 | 1 | sentinel llega con 13 true asi que este select no devuelve filas se hace con select where y no con un if antes del nodo po |
| 204 | replace | texto | 2 | 1 | ce con select where y no con un if antes del nodo porque el nodo corre una query por item de entrada el if solo no alcanza |
| 205 | replace | texto | 2 | 1 | do con posts reales que es justo el caso de un 429 en el 2o subreddit insert into posts id subreddit id title selftext url auth |
| 206 | replace | texto | 2 | 1 | t into posts id subreddit id title selftext url author hash score num comments created utc nlp category nlp score entities nl |
| 207 | replace | texto | 2 | 1 | um comments created utc nlp category nlp score entities nlp processed select 1 2 3 4 5 6 7 8 9 timestamptz 10 11 12 jsonb true |
| 208 | replace | texto | 2 | 1 | p processed select 1 2 3 4 5 6 7 8 9 timestamptz 10 11 12 jsonb true where coalesce 13 false false on conflict id do upda |
| 209 | replace | texto | 2 | 1 | terval 1 day and p ingested at date trunc day now at time zone america argentina buenos aires as n observado count filte |
| 210 | replace | texto | 2 | 1 | erval 11 day and p ingested at date trunc day now at time zone america argentina buenos aires interval 1 day 10 0 as base |
| 211 | replace | texto | 2 | 1 | terval 1 day at time zone america argentina buenos aires as ventana inicio date trunc day now at time zone america argentina |
| 212 | replace | texto | 2 | 1 | and p ingested at date trunc day now at time zone america argentina buenos aires interval 11 day group by p nlp category ord |
| 213 | replace | texto | 2 | 1 | toda la evaluaci n en anomalias genera alerta solo si hubo disparo ojo 1 la funci n que acepta jsonb se llama jsonb to recor |
| 214 | replace | texto | 2 | 1 | a funci n que acepta jsonb se llama jsonb to recordset json to recordset solo tiene la firma json invocarla con un jsonb |
| 215 | replace | texto | 2 | 1 | co se generan alertas repetidas porque el insert de alertas sale de ins que queda vacio si la evaluacion ya existia with |
| 216 | replace | texto | 2 | 1 | entana inicio timestamptz ventana fin timestamptz categoria varchar n observado int base media real umbral real disparo boolean |
| 217 | replace | texto | 2 | 1 | nsert into anomalias ventana inicio ventana fin categoria n observado base media umbral disparo select from reg where not exis |
| 218 | replace | texto | 2 | 1 | eturning id categoria n observado base media umbral disparo ventana inicio insert into alertas anomalia id canal destinatari |
| 219 | replace | texto | 2 | 1 | tfi jsonb build object categoria categoria n observado n observado base media base media umbral umbral ventana inicio ventana |
| 220 | replace | texto | 2 | 1 | bservado base media base media umbral umbral ventana inicio ventana inicio pendiente from ins where disparo returning id |
| 221 | replace | texto | 2 | 1 | tas q1 q15 del cap tulo de resultados ventana b5 corte 2026 10 17 todas son de solo lectura los literales de fecha fijan |
| 222 | replace | texto | 2 | 1 | son de solo lectura los literales de fecha fijan el estado congelado del 2026 10 19 de modo que la base pueda haber crecido sin |
| 223 | replace | texto | 2 | 1 | cundario congelado 31 filas persistidas hasta 2026 10 19 18 00 utc q1 totales select count filter where ingested at |
| 224 | replace | texto | 2 | 1 | 18 03 00 00 00 and ingested at 2026 10 19 00 00 00 00 as ventana count filter where created utc 2026 10 01 03 00 00 00 a |
| 225 | replace | texto | 2 | 1 | 01 03 00 00 00 and ingested at 2026 10 01 03 00 00 00 as previos count filter where ingested at 2026 10 19 00 00 00 00 a |
| 226 | replace | texto | 2 | 1 | 19 00 00 00 00 and ingested at 2026 10 19 18 00 00 00 as track select count from comments as comentarios count filter |
| 227 | replace | texto | 2 | 1 | sted at at time zone america argentina buenos aires date as dia count as n from posts where created utc 2026 10 18 03 0 |
| 228 | replace | texto | 2 | 1 | round avg extract epoch from ingested at created utc 60 0 numeric 2 as media round stddev samp extract epoch from ingested |
| 229 | replace | texto | 2 | 1 | round min extract epoch from ingested at created utc 60 0 numeric 2 as minimo round max extract epoch from ingested at crea |
| 230 | replace | texto | 2 | 1 | round max extract epoch from ingested at created utc 60 0 numeric 2 as maximo count filter where extract epoch from ingeste |
| 231 | delete | tabla | 5 | 0 | ontrasena cambiar mi contrasena acceso no autorizado acceso |
| 232 | delete | tabla | 5 | 0 | stan cifrados secuestro de datos extorsion wannacry lockbit |
| 233 | delete | tabla | 5 | 0 | acion exfiltrated leak leaked leaks breach breached exposed |
| 234 | delete | tabla | 5 | 0 | banco falso empleado falsa policia falso soporte pretexting |
| 235 | replace | tabla | 2 | 1 | ejecutable sobre tesi osint validaci n en consultas q1 q15 validacion md declaracion trazabilidad versiones md declaraci n jura |
| 236 | replace | tabla | 2 | 1 | validaci n en consultas q1 q15 validacion md declaracion trazabilidad versiones md declaraci n jurada de trazabilidad entre versi |
| 237 | replace | tabla | 2 | 1 | la 20261020 recalculo cifras v5 sql y recalculo cifras v5 resultados txt rec lculo independiente de las cifras clave del informe |
| 238 | replace | tabla | 2 | 1 | l informe consulta y salida literal correspondencia casos v5 csv c digo interno id url fecha y puntuaci n de los trece c |
| 239 | replace | tabla | 2 | 1 | asos permite abrir cada caso citado auditoria diccionario md auditor a completa de los 201 t rminos y efecto medido traz |
| 240 | replace | tabla | 2 | 1 | rcentiles n mediana y p95 por subconjunto motor anomalias recalculo md rec lculo del motor sobre created utc serie diaria y dis |
| 241 | replace | texto | 2 | 1 | v4 el directorio conserva el nombre v4 v5 es la versi n del documento anexos a ddl sql esquema f sico real anexo a b workfl |
| 242 | replace | texto | 2 | 1 | aluar muestra reproducible py ejecuta el nodo real sobre la muestra figuras figura 1 figura 4 png evidencias informe v4 20 |
| 243 | replace | texto | 2 | 1 | 0 19 consultas corpus b5 txt salida de las consultas q1 a q15 informe v5 2026 10 20 evidencia v5 zip copia congelada h |
| 244 | replace | texto | 2 | 1 | hash en d 1 anexo b c digo de los nodos y consultas q1 a q15 evidencia muestreo sorteo gu a hojas ciegas adjudicaci n y |
| 245 | insert | tabla | 0 | 2 | 8 sin respaldo rendimiento tabla 4 f1 score 0 815 umbral 0 800 generado el f1 medido es 0 711 tabla 5 8 sin respaldo ren |
| 246 | insert | tabla | 0 | 2 | ware a un hospital mendocino 05 05 2026 entidad enmascarada ilustraci n generada dem casos secci n 5 3 caso 3 filtraci n de un e |
| 247 | replace | tabla | 2 | 1 | nica del prototipo fuera de la ventana caracterizacion rate limit md psql 2026 09 25 caso 429 b4 derechogenial txt 25 09 20 |
| 248 | replace | tabla | 2 | 1 | a caracterizacion rate limit md psql 2026 09 25 caso 429 b4 derechogenial txt 25 09 2026 inicio de la ventana en curso 36 publicaci |
| 249 | insert | tabla | 0 | 5 | o del alcance baja de r argentina y r derechogenial alta de r netsec y r malware cambio de objeto registrado como in 07 ventana b5 md secci |
| 250 | replace | tabla | 2 | 1 | alibraci n no es el corpus de resultados evaluacion muestra control 2026 09 30 md y archivos asociados 01 10 2026 13 05 59 re |
| 251 | replace | tabla | 2 | 1 | l corte fuera del an lisis de este informe openspec changes recoleccion secundaria e 4 derivaci n de las cifras de la v4 y de la |
