SELECT count(DISTINCT cr.person_id)
FROM condition_records(192671) cr
JOIN study_population sp USING (person_id)
WHERE sp.gender_concept_id = 8532;
