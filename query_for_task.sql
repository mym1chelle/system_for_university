-- Выбрать всех студентов, обучающихся на курсе "Математика".
SELECT st.name, st.fathers_name, st.surname, c.name as course FROM student as st
JOIN student_to_course as sc ON sc.student_id = st.id
JOIN course as c ON sc.course_id = c.id
WHERE c.name = 'Математика';

-- Выбрать всех преподавателей, которые преподают в здании №3.
SELECT t.name, t.fathers_name, t.surname, b.number as building FROM teacher as t
JOIN course as c ON c.teacher_id = t.id
JOIN semester_to_course as s ON s.course_id = c.id
JOIN classroom as cl ON cl.id = s.classroom_id
JOIN building as b ON b.id = cl.building_id
WHERE b.number = 3;

-- Обновить оценку студента по курсу.
UPDATE course_grade
SET grade_id = grade_subq.id
FROM (SELECT id FROM grade WHERE grade = 'Оценка') as grade_subq 
WHERE course_grade.student_id = (
	SELECT id FROM student
	WHERE name = 'Имя' AND fathers_name = 'Отчество' AND surname = 'Фамилия'
) AND course_grade.course_id = (
	SELECT id FROM course
	WHERE name = 'Название курса'
);

-- Удалить задание для самостоятельной работы, которое было создано более года назад.
DELETE FROM task
WHERE created_at + INTERVAL '1 year' <= (SELECT CURRENT_DATE );

-- Добавить новый семестр в учебный год.
INSERT INTO semester (start_date, end_date) VALUES ('2024-01-14', '2024-07-09');