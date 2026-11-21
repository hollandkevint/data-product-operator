WITH observed AS (
  SELECT sum(least(op.observation_period_end_date, DATE '2018-12-31')
           - greatest(op.observation_period_start_date, DATE '2010-01-01') + 1) / 365.25 AS patient_years
  FROM observation_period op
  JOIN person p USING (person_id)
  WHERE op.observation_period_end_date >= DATE '2010-01-01'
    AND op.observation_period_start_date <= DATE '2018-12-31'
), visits AS (
  SELECT count(*) AS n
  FROM visit_occurrence
  WHERE visit_concept_id = 9201
    AND visit_start_date BETWEEN DATE '2010-01-01' AND DATE '2018-12-31'
)
SELECT 1000.0 * visits.n / observed.patient_years FROM visits, observed;
