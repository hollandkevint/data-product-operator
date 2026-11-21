SELECT count(DISTINCT co.person_id)
FROM condition_occurrence co
JOIN concept_ancestor ca ON ca.descendant_concept_id = co.condition_concept_id
WHERE ca.ancestor_concept_id = 28060;
