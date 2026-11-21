SELECT count(*) FROM observation_period
WHERE person_id NOT IN (SELECT person_id FROM person);
