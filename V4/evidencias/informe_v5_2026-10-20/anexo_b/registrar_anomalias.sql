-- Inserta TODA la evaluación en anomalias; genera alerta solo si hubo disparo.
-- OJO 1: la función que acepta jsonb se llama jsonb_to_recordset. json_to_recordset
-- solo tiene la firma (json); invocarla con un jsonb da
-- 'no existe la función json_to_recordset(jsonb)' y la evaluación no se registra.
-- OJO 2: *to_recordset exige un ARRAY json en el nivel superior. El nodo manda
-- JSON.stringify($json), que es un objeto suelto, y eso da
-- 'no se puede invocar jsonb_to_recordset en un no-array'. Por eso el
-- jsonb_build_array: envuelve el objeto en un array de un elemento.
-- El nodo corre la query una vez por item de entrada, asi que aqui llega
-- una sola categoria por vez y se inserta una fila por evaluacion.
-- OJO 3: la insercion es IDEMPOTENTE sobre (ventana_inicio, ventana_fin,
-- categoria). Sin este WHERE NOT EXISTS, ejecutar el workflow dos veces el
-- mismo dia inserta la misma evaluacion dos veces y el conteo de
-- suficiencia (que cuenta filas por dia) queda inflado. Con el guardia,
-- relanzar el nodo a mano para recuperar un dia perdido no duplica nada,
-- y tampoco se generan alertas repetidas porque el INSERT de alertas sale
-- de 'ins', que queda vacio si la evaluacion ya existia.
WITH reg AS (
  SELECT * FROM jsonb_to_recordset(jsonb_build_array($1::jsonb))
    AS x(ventana_inicio timestamptz, ventana_fin timestamptz, categoria varchar, n_observado int, base_media real, umbral real, disparo boolean)
),
ins AS (
  INSERT INTO anomalias (ventana_inicio, ventana_fin, categoria, n_observado, base_media, umbral, disparo)
  SELECT * FROM reg
  WHERE NOT EXISTS (
    SELECT 1 FROM anomalias a
    WHERE a.ventana_inicio = reg.ventana_inicio
      AND a.ventana_fin    = reg.ventana_fin
      AND a.categoria      = reg.categoria
  )
  RETURNING id, categoria, n_observado, base_media, umbral, disparo, ventana_inicio
)
INSERT INTO alertas (anomalia_id, canal, destinatario, payload, estado)
SELECT id, 'telegram', 'canal_tfi',
       jsonb_build_object('categoria', categoria, 'n_observado', n_observado, 'base_media', base_media, 'umbral', umbral, 'ventana_inicio', ventana_inicio),
       'PENDIENTE'
FROM ins
WHERE disparo
RETURNING id, anomalia_id, canal, payload, estado
