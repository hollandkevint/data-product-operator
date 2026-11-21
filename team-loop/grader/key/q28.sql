SELECT count(DISTINCT de.person_id)
FROM drug_exposure de
JOIN concept_ancestor ca ON ca.descendant_concept_id = de.drug_concept_id
WHERE ca.ancestor_concept_id IN (1115008, 1177480);
