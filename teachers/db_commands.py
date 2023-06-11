import psycopg2
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException
from teachers.schemas import GetTeacherConfig


def get_all_teachers_db(
        conn: psycopg2.connect,
        limit: int,
        offset: int
):
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


def get_teacher_db(
        conn: psycopg2.connect,
        teacher: GetTeacherConfig | None
):
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
