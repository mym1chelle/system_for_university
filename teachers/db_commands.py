import psycopg2
from psycopg2.extras import NamedTupleCursor


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
        surname: str | None,
        name: str | None,
        fathers_name: str | None
):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            SELECT * FROM teacher
            WHERE surname=COALESCE(%s, surname)
            AND name=COALESCE(%s, name)
            AND fathers_name=COALESCE(%s, fathers_name)
            ;
            """,
            (surname, name, fathers_name)
        )
        return cur.fetchone()
