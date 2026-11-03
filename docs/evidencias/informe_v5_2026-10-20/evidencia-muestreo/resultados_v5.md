# Resultados de la validacion V5

- Casos etiquetados (anotador 3): **352**
- Submuestra comun (3 anotadores): **50**
- Kappa de Fleiss: **0.509** (moderado)
- Desacuerdos: **20** | resueltos: 20 | pendientes: 0

## Matriz de confusion

| Estrato | n | Amenaza real | No relevante |
|---|---|---|---|
| 1 (positivos del clasificador, censo) | 170 | 144 | 26 |
| 2 (negativos del clasificador, muestra) | 182 | 30 | 152 |

## Estimadores

| Metrica | Valor | IC 95 % |
|---|---|---|
| Precision | 84.7 % | [78.4; 89.8] |
| Sensibilidad | 61.2 % | [53.4; 69.5] |
| F1 | 0.711 | [0.635; 0.783] |
| Omision estrato 2 | 16.5 % | [11.4; 22.7] |

Peso de muestreo w = N0/n0 = 554/182 = 3.044

## Por comunidad

| Comunidad | Censo n | TP | FP | Precision | Muestra n | Omitidos | Omision |
|---|---:|---:|---:|---:|---:|---:|---:|
| r/Malware | 97 | 81 | 16 | 83.5 % | 18 | 13 | 72.2 % |
| r/devsarg | 7 | 3 | 4 | 42.9 % | 135 | 2 | 1.5 % |
| r/netsec | 66 | 60 | 6 | 90.9 % | 29 | 15 | 51.7 % |

## Otros indicadores

- Tasa de falsos descubrimientos (1 − precision): **15.3 %**
- Acierto exacto de categoria (sobre 144 amenazas detectadas por ambos): **116/144 = 80.6 %**
- Amenazas estimadas en el corpus: **235.3** de 724 (32.5 %)
- Distribucion de la referencia: {'Phishing': 9, 'No relevante': 178, 'Vulnerabilidades': 67, 'Malware': 90, 'Robo de Credenciales': 1, 'Infraestructura y Ataques': 4, 'Filtración de Datos': 1, 'Ransomware': 2}

## Matriz por categoria (referencia x clasificador)

| Referencia \ Clasificador | Filtración de Datos | Hacktivismo | Infraestructura y Ataques | Malware | No relevante | Phishing | Ransomware | Robo de Credenciales | Vulnerabilidades |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Filtración de Datos | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| Infraestructura y Ataques | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| Malware | 0 | 0 | 1 | 59 | 14 | 5 | 2 | 2 | 7 |
| No relevante | 2 | 1 | 1 | 16 | 152 | 0 | 0 | 1 | 5 |
| Phishing | 0 | 0 | 0 | 1 | 3 | 5 | 0 | 0 | 0 |
| Ransomware | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| Robo de Credenciales | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Vulnerabilidades | 1 | 0 | 0 | 2 | 12 | 2 | 0 | 1 | 49 |
