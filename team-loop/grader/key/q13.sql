SELECT count(DISTINCT co.person_id)
FROM condition_occurrence co
JOIN concept_ancestor ca ON ca.descendant_concept_id = co.condition_concept_id
JOIN person p ON p.person_id = co.person_id
WHERE ca.ancestor_concept_id = 192671
  AND p.gender_concept_id = 8532;
