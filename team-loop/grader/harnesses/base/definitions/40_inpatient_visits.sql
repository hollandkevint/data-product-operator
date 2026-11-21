-- Inpatient visits. Length of stay counts both the admit day and the discharge day.
CREATE VIEW inpatient_visits AS
SELECT *, visit_end_date - visit_start_date + 1 AS los_days
FROM visit_occurrence
WHERE visit_concept_id = 9201;
