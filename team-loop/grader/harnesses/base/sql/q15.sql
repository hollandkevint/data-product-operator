SELECT count(*) FROM (
  SELECT person_id, min(condition_start_date) AS first_date
  FROM condition_records(192671)
  GROUP BY person_id
) WHERE first_date BETWEEN DATE '2010-01-01' AND DATE '2018-12-31';
