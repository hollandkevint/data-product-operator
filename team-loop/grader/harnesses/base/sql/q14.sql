SELECT 100.0 * count(DISTINCT b.person_id) / count(DISTINCT s.person_id)
FROM condition_records(4283893) s
LEFT JOIN condition_records(260139) b USING (person_id);
