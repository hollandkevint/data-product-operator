SELECT count(*)
FROM drug_exposure de
JOIN concept_ancestor ca ON ca.descendant_concept_id = de.drug_concept_id
WHERE ca.ancestor_concept_id = 1125315;
