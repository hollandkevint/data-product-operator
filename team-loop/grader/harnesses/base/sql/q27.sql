SELECT 100.0 * count(*) FILTER (WHERE sp.gender_concept_id = 8532) / count(*)
FROM (SELECT DISTINCT person_id FROM ingredient_eras(1118084)) u
JOIN study_population sp USING (person_id);
