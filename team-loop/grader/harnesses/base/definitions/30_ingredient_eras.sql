-- Drug eras for one ingredient. drug_era is already rolled up to ingredient level.
CREATE MACRO ingredient_eras(cid) AS TABLE
SELECT * FROM drug_era WHERE drug_concept_id = cid;
