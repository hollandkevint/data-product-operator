-- Inpatient visits. Length of stay is discharge date minus admit date.
CREATE VIEW inpatient_visits AS
SELECT *, visit_end_date - visit_start_date AS los_days
FROM visit_occurrence
WHERE visit_concept_id = 9201;
