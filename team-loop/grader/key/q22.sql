WITH ordered AS (
  SELECT person_id, visit_start_date,
         lag(visit_end_date) OVER (PARTITION BY person_id ORDER BY visit_start_date, visit_occurrence_id) AS prior_end
  FROM visit_occurrence
  WHERE visit_concept_id = 9201
)
SELECT median(visit_start_date - prior_end) FROM ordered WHERE prior_end IS NOT NULL;
