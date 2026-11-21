SELECT count(DISTINCT cr.person_id)
FROM condition_records(192671) cr
JOIN (
  SELECT person_id, min(drug_era_start_date) AS first_date
  FROM ingredient_eras(1118084)
  GROUP BY person_id
) fc USING (person_id)
WHERE cr.condition_start_date >= fc.first_date;
