-- Study population: patients observed at any time in the 2010-2018 analysis window,
-- with their observation time inside that window in patient-years.
CREATE VIEW study_population AS
SELECT p.person_id, p.gender_concept_id, p.year_of_birth,
       (least(op.observation_period_end_date, DATE '2018-12-31')
        - greatest(op.observation_period_start_date, DATE '2010-01-01') + 1) / 365.25 AS window_years
FROM person p
JOIN observation_period op USING (person_id)
WHERE op.observation_period_end_date >= DATE '2010-01-01'
  AND op.observation_period_start_date <= DATE '2018-12-31';
