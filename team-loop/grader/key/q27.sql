WITH users AS (
  SELECT DISTINCT de.person_id
  FROM drug_exposure de
  JOIN concept_ancestor ca ON ca.descendant_concept_id = de.drug_concept_id
  WHERE ca.ancestor_concept_id = 1118084
)
SELECT 100.0 * count(*) FILTER (WHERE p.gender_concept_id = 8532) / count(*)
FROM users u
JOIN person p USING (person_id);
