-- Guardia anti-centinela (IN-08). El item de error que genera 'Parse Reddit Posts'
-- cuando Reddit responde 429 viaja por toda la cadena para que el loop no se
-- corte, pero NO debe terminar en la tabla: el sub que fallo vale como 0 posts.
-- El sentinel llega con $13 = TRUE, asi que este SELECT no devuelve filas.
-- Se hace con SELECT ... WHERE y no con un IF antes del nodo porque el nodo
-- corre una query por item de entrada: el IF solo no alcanza si el item llega
-- mezclado con posts reales, que es justo el caso de un 429 en el 2o subreddit.
INSERT INTO posts (id, subreddit_id, title, selftext, url, author_hash, score, num_comments, created_utc, nlp_category, nlp_score, entities, nlp_processed)
SELECT $1, $2, $3, $4, $5, $6, $7, $8, $9::timestamptz, $10, $11, $12::jsonb, TRUE
WHERE COALESCE($13, FALSE) = FALSE
ON CONFLICT (id) DO UPDATE SET
  title = EXCLUDED.title,
  selftext = EXCLUDED.selftext,
  url = EXCLUDED.url,
  score = EXCLUDED.score,
  num_comments = EXCLUDED.num_comments,
  nlp_category = EXCLUDED.nlp_category,
  nlp_score = EXCLUDED.nlp_score,
  entities = EXCLUDED.entities,
  nlp_processed = TRUE
