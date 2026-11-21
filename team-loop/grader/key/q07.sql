SELECT count(*)
FROM observation_period op
WHERE NOT EXISTS (SELECT 1 FROM person p WHERE p.person_id = op.person_id);
