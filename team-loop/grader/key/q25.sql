WITH first_celecoxib AS (
  SELECT de.person_id, min(de.drug_exposure_start_date) AS first_date
  FROM drug_exposure de
  JOIN concept_ancestor ca ON ca.descendant_concept_id = de.drug_concept_id
  WHERE ca.ancestor_concept_id = 1118084
  GROUP BY de.person_id
)
SELECT count(DISTINCT co.person_id)
FROM condition_occurrence co
JOIN concept_ancestor ca ON ca.descendant_concept_id = co.condition_concept_id
JOIN first_celecoxib fc ON fc.person_id = co.person_id
WHERE ca.ancestor_concept_id = 192671
  AND co.condition_start_date >= fc.first_date;
