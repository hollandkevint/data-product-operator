-- Synthetic only. Run: duckdb :memory: < check.sql
CREATE TEMP TABLE events AS
SELECT * FROM read_csv('example.csv',
  columns = {'patient_key':'VARCHAR', 'amount_raw':'VARCHAR'},
  header = true, delim = ',', nullstr = '');
CREATE TEMP TABLE roster AS
SELECT * FROM (VALUES ('001'),('001'),('1')) t(patient_key);
SELECT CASE WHEN (SELECT count(*) FROM events WHERE patient_key = '001') = 1
  AND (SELECT count(*) FROM events WHERE patient_key = '1') = 1
  THEN 'PASS identifier preserved' ELSE error('Identifier changed') END;
SELECT CASE WHEN (SELECT count(*) FROM events
  WHERE amount_raw IS NOT NULL AND try_cast(amount_raw AS DECIMAL(12,2)) IS NULL) = 1
  THEN 'PASS invalid cast counted' ELSE error('Invalid cast hidden') END;
SELECT CASE WHEN (SELECT count(*) FROM
  (SELECT patient_key FROM roster GROUP BY patient_key HAVING count(*) > 1)) = 1
  THEN 'PASS duplicate key detected' ELSE error('Duplicate key missed') END;
SELECT CASE WHEN
  (SELECT sum(try_cast(amount_raw AS DECIMAL(12,2))) FROM events) = 10.00 AND
  (SELECT sum(try_cast(e.amount_raw AS DECIMAL(12,2)))
   FROM events e JOIN roster r USING(patient_key)) = 20.00
  THEN 'PASS join inflation exposed' ELSE error('Join inflation check failed') END;
SELECT CASE WHEN (SELECT count(*) FROM events e ANTI JOIN roster r USING(patient_key)) = 1
  THEN 'PASS unmatched key detected' ELSE error('Unmatched key missed') END;
