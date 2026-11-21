SELECT 1000.0
  * (SELECT count(*) FROM inpatient_visits WHERE visit_start_date BETWEEN DATE '2010-01-01' AND DATE '2018-12-31')
  / (SELECT count(*) FROM study_population);
