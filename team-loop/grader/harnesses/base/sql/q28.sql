SELECT count(DISTINCT person_id) FROM (
  SELECT person_id FROM ingredient_eras(1115008)
  UNION ALL
  SELECT person_id FROM ingredient_eras(1177480)
);
