-- Condition records for one concept and every descendant of it in concept_ancestor.
-- concept_ancestor carries a self row, so the concept itself is included.
CREATE MACRO condition_records(cid) AS TABLE
SELECT co.*
FROM condition_occurrence co
JOIN concept_ancestor ca ON ca.descendant_concept_id = co.condition_concept_id
WHERE ca.ancestor_concept_id = cid;
