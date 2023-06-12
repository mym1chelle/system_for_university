import psycopg2
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException
from teachers.db_commands import (
    get_teacher_info_or_empty_dict_by_id,
    get_teacher_info_or_empty_dict
)
from courses.schemas import CreateCourse, CourseData


def get_course_by_name(
        conn: psycopg2.connect,
        name: str
):
    """Возвращает данные о курсе по названию курса"""
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
                SELECT * FROM course
                WHERE name=(%s);
                """, (name,)
        )
        return cur.fetchone()


def get_course_by_id_or_404(
        conn: psycopg2.connect,
        id: int
):
    """
    Возвращает данные о курсе по ID
    Если такой курс с таким ID не найден вызывает ошибку 404
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
                detail=f'The course with ID {id} does not exist'
            )
        else:
            teacher = get_teacher_info_or_empty_dict_by_id(
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


def add_new_course(
        conn: psycopg2.connect,
        course: CreateCourse,
        teacher: int | None
):
    """Добавляет новый курс в базу данных

    Для создания нового курса нужно получить информацию о программе курса
    и преподавателе, который ведет курс

    В данной функции проводится поиск данных по переданным параметрам и
    валидация
    """
    is_course_exist = get_course_by_name(conn=conn, name=course.course_name)
    if is_course_exist:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f'The course «{course.course_name}» already exists'
        )
    else:
        course_programme = get_course_programme_info_or_empty_dict(
            conn=conn,
            id=get_course_programme_id_or_none_or_404(
                conn=conn,
                course=course
            )
        )
        course_teacher = get_teacher_info_or_empty_dict(
            conn=conn,
            teacher=teacher
        )
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO course (name, course_programme_id, teacher_id)
                VALUES (%s, %s, %s);
                """,
                (
                    course.course_name,
                    course_programme.get('id'),
                    course_teacher.get('id')
                )
            )
        conn.commit()
        course = get_course_by_name(conn=conn, name=course.course_name)
        return {
            'id': course.id,
            'name': course.name,
            'course_programme': course_programme,
            'teacher': course_teacher
        }


def get_course_programme_id_or_none_or_404(
        conn: psycopg2.connect,
        course: CourseData
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
                detail=f'The course programme «{name}» does not exist'
            )
    return name


def get_course_programme_info_or_empty_dict(
        conn: psycopg2.connect,
        id: int
):
    """
    Возвращает по ID данные о программе курса
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
    """
    Возвращает список словарей с информацией о студентах,
    которые проходят выбранный курс
    Если студентов нет на данном курсе — вернет пустой список
    """
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
