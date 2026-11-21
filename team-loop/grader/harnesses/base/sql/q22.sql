SELECT median(v.visit_start_date - prior.visit_end_date)
FROM inpatient_visits v
JOIN inpatient_visits prior ON prior.visit_occurrence_id = v.preceding_visit_occurrence_id;
