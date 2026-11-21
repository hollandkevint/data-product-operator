SELECT count(*) FROM (
  SELECT person_id FROM inpatient_visits GROUP BY person_id HAVING count(*) >= 2
);
