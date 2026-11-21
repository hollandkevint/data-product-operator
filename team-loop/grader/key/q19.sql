SELECT count(*) FROM (
  SELECT person_id FROM visit_occurrence WHERE visit_concept_id = 9201
  GROUP BY person_id HAVING count(*) >= 2
);
