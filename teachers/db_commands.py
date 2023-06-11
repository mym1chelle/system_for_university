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
