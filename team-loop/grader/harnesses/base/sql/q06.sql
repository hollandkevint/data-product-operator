SELECT median(op.observation_period_end_date - op.observation_period_start_date)
FROM observation_period op
JOIN study_population sp USING (person_id);
