-- Condition records for one concept, matched on the concept id as recorded.
CREATE MACRO condition_records(cid) AS TABLE
SELECT * FROM condition_occurrence WHERE condition_concept_id = cid;
