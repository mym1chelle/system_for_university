import psycopg2
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException
from teachers.schemas import GetTeacher


def get_grade_by_name(
        conn: psycopg2.connect,
        grade_name: str
):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            SELECT * FROM grade
            WHERE grade=(%s);
            """,
            (grade_name,)
        )
        return cur.fetchone()


def create_new_grade(
        conn: psycopg2.connect,
        grade_name: str
):
    grade = get_grade_by_name(conn=conn, grade_name=grade_name)
    if grade:
        raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'The grade {grade_name} already exists'
            )
    else:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO grade (grade)
                VALUES (%s);
                """,
                (grade_name,)
            )
        conn.commit()
        new_grade = get_grade_by_name(
            conn=conn,
            grade_name=grade_name
        )
        return {
            'id': new_grade.id,
            'grade': new_grade.grade
        }


def get_teacher_info_or_empty_dict(
        conn: psycopg2.connect,
        id: int
):
    """
    Возвращает информацию о преподавателе в виде словаря по ID
    если ID = None – вернет пустой словарь
    """
    if id:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """
                SELECT *
                FROM teacher
                WHERE id=(%s);
                """, (id,)
            )
            teacher = cur.fetchone()
        course_teacher = {
            'id': teacher.id,
            'surname': teacher.surname,
            'name': teacher.name,
            'fathers_name': teacher.fathers_name
        }
    else:
        course_teacher = {}
    return course_teacher


def get_teacher_id_or_none(
        conn: psycopg2.connect,
        teacher: GetTeacher | None
):
    """
    Возвращает ID преподавателя по переданным данным
    Если преподавателей с такими данными несколько — вернет первого найденного
    Если преподавателя с такими данными нет — вызовет ошибку 404

    Иначе вернет None
    """
    if teacher:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """
                SELECT id FROM teacher
                WHERE surname=COALESCE(%s, surname)
                AND name=COALESCE(%s, name)
                AND fathers_name=COALESCE(%s, fathers_name)
                ;
                """,
                (teacher.surname, teacher.name, teacher.fathers_name)
            )
            is_teacher_exist = cur.fetchone()
        if is_teacher_exist:
            return is_teacher_exist.id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='The teacher does not exist'
            )
    else:
        return teacher


def get_teacher_by_id(
        conn: psycopg2.connect,
        id: int
):
    """Возвращает информацию о преподавателе по ID"""
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
                SELECT * FROM teacher
                WHERE id=(%s);
                """,
            (id)
        )
        return cur.fetchone()
