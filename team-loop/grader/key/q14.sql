WITH sinusitis AS (
  SELECT DISTINCT co.person_id
  FROM condition_occurrence co
  JOIN concept_ancestor ca ON ca.descendant_concept_id = co.condition_concept_id
  WHERE ca.ancestor_concept_id = 4283893
), bronchitis AS (
  SELECT DISTINCT co.person_id
  FROM condition_occurrence co
  JOIN concept_ancestor ca ON ca.descendant_concept_id = co.condition_concept_id
  WHERE ca.ancestor_concept_id = 260139
)
SELECT 100.0 * count(b.person_id) / count(*)
FROM sinusitis s
LEFT JOIN bronchitis b USING (person_id);
