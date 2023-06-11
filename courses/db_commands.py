import psycopg2
from datetime import date
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException


def add_course_db(
        conn: psycopg2.connect,
        name: str,
        course_programme_id: int | None,
        teacher_id: int | None
):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO course (name, course_programme_id, teacher_id)
            VALUES (%s, %s, %s);
            """,
            (name, course_programme_id, teacher_id)
        )
    conn.commit()


def get_course_programme_db(
        conn: psycopg2.connect,
        name: str
):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            SELECT id, name FROM course_programme
            WHERE name=(%s);
            """, (name,)
        )
        return cur.fetchone()
