-- Study population: every patient in the person table.
CREATE VIEW study_population AS
SELECT person_id, gender_concept_id, year_of_birth
FROM person;
