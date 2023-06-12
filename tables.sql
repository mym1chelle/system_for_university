CREATE TABLE IF NOT EXISTS faculty (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS curriculum (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL,
    link_by_file VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS department (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) NOT NULL,
    faculty_id bigint REFERENCES faculty(id) ON DELETE CASCADE,
    curriculum_id bigint REFERENCES curriculum(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS students_group (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    code int NOT NULL,
    department_id bigint REFERENCES department(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS student (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    surname VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    fathers_name VARCHAR(50),
    date_of_birth DATE NOT NULL,
    group_id bigint REFERENCES students_group(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS semester (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    start_date DATE NOT NULL UNIQUE,
    end_date DATE NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS schedule (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    semester_id bigint REFERENCES semester(id) UNIQUE
);

CREATE TABLE IF NOT EXISTS building (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    number int NOT NULL,
    address VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS classroom (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    number int NOT NULL,
    building_id bigint REFERENCES building(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS grade (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    grade VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS teacher (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    surname VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    fathers_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS course_programme (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL,
    link_by_file VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS course (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL UNIQUE,
    course_programme_id bigint REFERENCES course_programme(id),
    teacher_id bigint REFERENCES teacher(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS student_to_course (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    student_id bigint REFERENCES student(id) ON DELETE CASCADE,
    course_id bigint REFERENCES course(id) ON DELETE CASCADE,
    CONSTRAINT student_course_unique UNIQUE (student_id, course_id)
    -- ограничение на комбинацию учебный студент-курс, чтобы студень не мог проходить несколько раз один и тот же курс
);

CREATE TABLE IF NOT EXISTS curriculum_to_course (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    course_id bigint REFERENCES course(id) ON DELETE CASCADE,
    curriculum_id bigint REFERENCES curriculum(id) ON DELETE SET NULL,
    CONSTRAINT curriculum_course_unique UNIQUE (curriculum_id, course_id)
    -- ограничение на комбинацию учебный план-курс, чтобы в одном учебном плане не было несколько одинаковых курсов
);

CREATE TABLE IF NOT EXISTS semester_to_course (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    course_id bigint REFERENCES course(id),
    classroom_id bigint REFERENCES classroom(id),
    semester_id bigint REFERENCES semester(id),
    CONSTRAINT semester_course_unique UNIQUE (semester_id, course_id)
    -- ограничение на комбинацию семестр-курс, чтобы в одном семестре не было несколько одинаковых курсов
);

CREATE TABLE IF NOT EXISTS task (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    task TEXT NOT NULL,
    course_id bigint REFERENCES course(id) ON DELETE CASCADE,
    created_at DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS task_grade (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    student_id bigint REFERENCES student(id) ON DELETE CASCADE,
    task_id bigint REFERENCES task(id) ON DELETE CASCADE,
    grade_id bigint REFERENCES grade(id) ON DELETE SET NULL,
    CONSTRAINT student_task_unique UNIQUE (student_id, task_id)
    -- ограничение на комбинацию задание-студент, чтобы студент не мог получить несколько оценок за одно и то же задание
);

CREATE TABLE IF NOT EXISTS exam (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    course_id bigint REFERENCES course(id) ON DELETE CASCADE,
    date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS exam_grade (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    student_id bigint REFERENCES student(id) ON DELETE CASCADE,
    exam_id bigint REFERENCES exam(id) ON DELETE CASCADE,
    grade_id bigint REFERENCES grade(id) ON DELETE SET NULL,
    CONSTRAINT student_exam_unique UNIQUE (student_id, exam_id)
    -- ограничение на комбинацию экзамен-студент, чтобы студент не мог получить несколько оценок за один и тот же экзамен
);


CREATE TABLE IF NOT EXISTS course_grade (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    student_id bigint REFERENCES student(id) ON DELETE CASCADE,
    course_id bigint REFERENCES course(id) ON DELETE CASCADE,
    grade_id bigint REFERENCES grade(id) ON DELETE SET NULL,
    CONSTRAINT student_course_grade_unique UNIQUE (student_id, course_id)
    -- ограничение на комбинацию курс-студент, чтобы студент не мог получить несколько оценок за один и тот же курс
);