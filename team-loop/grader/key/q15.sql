WITH first_bleed AS (
  SELECT co.person_id, min(co.condition_start_date) AS first_date
  FROM condition_occurrence co
  JOIN concept_ancestor ca ON ca.descendant_concept_id = co.condition_concept_id
  WHERE ca.ancestor_concept_id = 192671
  GROUP BY co.person_id
)
SELECT count(*) FROM first_bleed WHERE first_date BETWEEN DATE '2010-01-01' AND DATE '2018-12-31';
