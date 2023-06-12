import psycopg2
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException
from teachers.schemas import GetTeacher


def get_all_teachers_db(
        conn: psycopg2.connect,
        limit: int,
        offset: int
):
    """
    Вернет список словарей с даммыми всех учителей
    """
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            SELECT * FROM teacher
            ORDER BY id
            LIMIT (%s)
            OFFSET (%s)
            ;
            """,
            (limit, offset)
        )
        return cur.fetchall()


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
