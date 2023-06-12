import psycopg2
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException
from teachers.schemas import GetTeacher
from teachers.db_commands import get_teacher_id_or_none, get_teacher_info_or_empty_dict
from courses.schemas import CreateCourse, CreateCourseResult, GetCourse


def get_course_by_name(
        conn: psycopg2.connect,
        name: str
):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
                SELECT * FROM course
                WHERE name=(%s);
                """, (name,)
        )
        return cur.fetchone()


def get_course_by_id(
        conn: psycopg2.connect,
        id: str
):
    """
    Возвращает данные о курсе по ID
    Если такой курс с таким ID не найден
    вызывает ошибку 404
    """
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
                SELECT *
                FROM course
                WHERE id=(%s);
                """, (id,)
        )
        course = cur.fetchone()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='The course programme does not exist'
            )
        else:
            teacher = get_teacher_info_or_empty_dict(
                conn=conn,
                id=course.teacher_id
            )
            course_programme = get_course_programme_info_or_empty_dict(
                conn=conn,
                id=course.course_programme_id
            )
            return {
                'id': course.id,
                'name': course.name,
                'course_programme': course_programme,
                'teacher': teacher
            }


def get_course_programme_by_id(
        conn: psycopg2.connect,
        id: int
):
    """
    Возвращает данные о программе курса по ID
    """
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
                SELECT * FROM course_programme
                WHERE id=(%s);
                """, (id,)
        )
        return cur.fetchone()


def add_course_db(
        conn: psycopg2.connect,
        course: CreateCourse,
        teacher: GetTeacher | None
):
    is_course_exist = get_course_by_name(conn=conn, name=course.curse_name)
    print(is_course_exist)
    if is_course_exist:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f'The course already exist: {course.curse_name}'
        )
    else:
        course_programme_id = get_course_programme_id_or_none(
            conn=conn,
            course=course
        )
        course_teacher_id = get_teacher_id_or_none(
            conn=conn,
            teacher=teacher
        )
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO course (name, course_programme_id, teacher_id)
                VALUES (%s, %s, %s);
                """,
                (course.curse_name, course_programme_id, course_teacher_id)
            )
        conn.commit()
        return CreateCourseResult(
            curse_name=course.curse_name,
            course_programme_id=course_programme_id,
            teacher_id=course_teacher_id
        )


def get_course_programme_id_or_none(
        conn: psycopg2.connect,
        course: GetCourse
):
    """
    Возвращает ID программы для выбранного курса
    Если такой программы нет — вызовет ошибку 404
    если у курса нет программы вернет None
    """
    name = course.course_programme_name
    if name:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """
                SELECT id FROM course_programme
                WHERE name=(%s);
                """, (name,)
            )
            course_programme = cur.fetchone()
        if course_programme:
            return course_programme.id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The course programme does not exist: {name}'
            )
    return name


def get_course_programme_info_or_empty_dict(
        conn: psycopg2.connect,
        id: int
):
    """Возвращает по ID данные о программе курса
    Если переданный ID = None, то вернет пустой словарь
    """
    if id:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """
                SELECT *
                FROM course_programme
                WHERE id=(%s);
                """, (id,)
            )
            programme = cur.fetchone()
        course_programme = {
            'id': programme.id,
            'name': programme.name,
            'link_by_file': programme.link_by_file
        }
    else:
        course_programme = {}
    return course_programme


def get_all_sudents_in_course(
        conn: psycopg2.connect,
        course_id: int,
        limit: int,
        offset: int,
):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
                SELECT st.id, st.surname, st.name, st.fathers_name, st.date_of_birth, gp.code FROM course as cr
                JOIN student_to_course as stct ON stct.course_id = cr.id
                JOIN student as st ON st.id = stct.student_id
                LEFT JOIN students_group as gp ON gp.id=st.group_id
                WHERE cr.id=(%s)
                ORDER BY id
                LIMIT (%s)
                OFFSET (%s);
                """, (course_id, limit, offset)
        )
        students = cur.fetchall()
        return [
            {
                'id': student.id,
                'surname': student.surname,
                'name': student.name,
                'fathers_name': student.fathers_name,
                'date_of_birth': student.date_of_birth,
                'group_code': student.code

            } for student in students
        ]
