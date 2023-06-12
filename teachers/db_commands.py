import psycopg2
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException
from teachers.schemas import TeacherID


def get_all_teachers_db(
        conn: psycopg2.connect,
        limit: int,
        offset: int
):
    """
    Возвращает список словарей с данными всех преподавателей
    Если преподавателей нет — вернет пустой список
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
        teachers = cur.fetchall()
        return [
            {
                'id': teacher.id,
                'surname': teacher.surname,
                'name': teacher.name,
                'fathers_name': teacher.fathers_name

            } for teacher in teachers
        ]


def get_teacher_info_or_empty_dict_by_id(
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
        if teacher:
            course_teacher = {
                'id': teacher.id,
                'surname': teacher.surname,
                'name': teacher.name,
                'fathers_name': teacher.fathers_name
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The teacher with ID «{id}» does not exist'
            )
    else:
        course_teacher = {}
    return course_teacher


def get_teacher_info_or_empty_dict(
    conn: psycopg2.connect,
    teacher: TeacherID
):
    """
    Возвращает данные о преподавателе по ID
    Если преподаватель с таким ID не был найден
    вернет пустой словарь
    """
    if teacher is None:
        return {}
    else:
        return get_teacher_info_or_empty_dict_by_id(
            conn=conn,
            id=teacher.id
        )
