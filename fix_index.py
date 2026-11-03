with open('docs/informe/tesis_v6.md','r',encoding='utf-8') as f:
    c = f.read()
old = '''## Índice general

1. Introducción

2. Marco teórico y estado del arte

3. Marco metodológico

4. Desarrollo del sistema

5. Resultados

6. Discusión

7. Conclusiones

8. Recomendaciones y trabajos futuros

9. Referencias bibliográficas

10. Anexos A–E'''
new = '''## Índice general

- Resumen
- Abstract
- Declaración de autoría y de uso de herramientas de asistencia
- Siglas
- 1. Introducción
  - 1.1. Contextualización del problema
  - 1.2. Planteamiento del problema
  - 1.3. Justificación del proyecto
  - 1.4. Delimitación y alcance
  - 1.5. Objetivos de la investigación
  - 1.6. Supuesto de trabajo y criterios de éxito
  - 1.7. Preguntas de investigación
- 2. Marco teórico y estado del arte
  - 2.1. Marco conceptual
    - 2.1.1. Inteligencia de fuentes abiertas (OSINT)
    - 2.1.2. Reddit como fuente de inteligencia
    - 2.1.3. Ciencia de datos, minería de datos y procesamiento de lenguaje natural
    - 2.1.4. Arquitecturas ETL y herramientas de automatización
  - 2.2. Estado del arte y brecha de conocimiento
- 3. Marco metodológico
  - 3.1. Tipo y diseño de la investigación
  - 3.2. Operacionalización del protocolo de recolección
  - 3.3. Protocolo de validación del clasificador NLP
    - 3.3.1. Protocolo diseñado
    - 3.3.2. Ejecución real
    - 3.3.3. Consecuencias declaradas del diseño
    - 3.3.4. Reproducibilidad de la medición
    - 3.3.5. Definición operativa de las métricas
  - 3.4. Aspectos legales, regulatorios y éticos
- 4. Desarrollo del sistema
  - 4.1. Arquitectura general
  - 4.2. Modelo de datos
  - 4.3. Flujo de ingesta
  - 4.4. Clasificador por diccionario
    - 4.4.1. Decisiones de diseño del clasificador y sus consecuencias
  - 4.5. Motor de detección de anomalías
- 5. Resultados
  - 5.1. Corpus analizado
    - 5.1.1. Régimen de operación por día (instancia de n8n)
  - 5.2. Composición del corpus
  - 5.3. Latencia extremo a extremo
  - 5.4. Motor de anomalías
  - 5.5. Validación del clasificador
    - 5.5.1. Muestra de control (30/09/2026) — antecedente
    - 5.5.2. Validación vigente sobre B5
  - 5.6. Extracción de entidades
  - 5.7. Casos representativos
  - 5.8. Síntesis del cumplimiento
- 6. Discusión
  - 6.1. Desempeño del sistema frente a los criterios
  - 6.2. Aporte al léxico rioplatense
  - 6.3. Limitaciones
  - 6.4. Contraste con el trabajo antecedente
- 7. Conclusiones
  - 7.1. Trazabilidad de los criterios de éxito
  - 7.2. Trazabilidad de los objetivos específicos
  - 7.3. Respuesta a las preguntas de investigación
  - 7.4. Conclusión general
- 8. Recomendaciones y trabajos futuros
- 9. Referencias bibliográficas
- 10. Anexos A–E'''
if old in c:
    c2 = c.replace(old,new)
    with open('docs/informe/tesis_v6.md','w',encoding='utf-8') as f:
        f.write(c2)
    print('ok')
else:
    print('no')
