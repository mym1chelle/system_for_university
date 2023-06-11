import psycopg2
from datetime import date
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException


def get_group_via_code_db(conn: psycopg2.connect, group_code: int):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            "SELECT id, code FROM students_group WHERE code=(%s);",
            (group_code,)
        )
        return cur.fetchone()


def get_student_db(conn: psycopg2.connect, student_id: int):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            SELECT st.id, st.name, st.surname, st.fathers_name, st.date_of_birth, gp.code
            FROM student as st
            LEFT JOIN students_group as gp ON gp.id=st.group_id
            WHERE st.id=(%s)
            ;
            """,
            (student_id,)
        )
        return cur.fetchone()


def add_student_db(
        conn: psycopg2.connect,
        surname: str,
        name: str,
        fathers_name: str | None,
        date_of_birth: date,
        group_id: int | None
):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO student (
                surname, name, fathers_name, date_of_birth, group_id
            ) VALUES (%s, %s, %s, %s, %s);
            """,
            (
                surname,
                name,
                fathers_name,
                date_of_birth,
                group_id
            )
        )
    conn.commit()


def update_student(
        conn: psycopg2.connect,
        surname: str | None,
        name: str | None,
        fathers_name: str | None,
        date_of_birth: date | None,
        group_id: int | None,
        student_id: int
):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            UPDATE student SET
                surname=COALESCE(%s, surname),
                name=COALESCE(%s, name),
                fathers_name=COALESCE(%s, fathers_name),
                date_of_birth=COALESCE(%s, date_of_birth),
                group_id=COALESCE(%s, group_id)
            WHERE id=(%s);
            """,
            (
                surname,
                name,
                fathers_name,
                date_of_birth,
                group_id,
                student_id,
            )
        )
        conn.commit()


def edit_student_db(
        conn: psycopg2.connect,
        surname: str | None,
        name: str | None,
        fathers_name: str | None,
        date_of_birth: date | None,
        group_code: int | None,
        student_id: int
):
    if group_code is not None:
        group = get_group_via_code_db(conn=conn, group_code=group_code)
        if group:
            update_student(
                conn=conn,
                surname=surname,
                name=name,
                fathers_name=fathers_name,
                date_of_birth=date_of_birth,
                group_id=group.id,
                student_id=student_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'There is no group with this code: {group_code}'
            )
    else:
        update_student(
                conn=conn,
                surname=surname,
                name=name,
                fathers_name=fathers_name,
                date_of_birth=date_of_birth,
                group_id=group_code,
                student_id=student_id
            )
    return get_student_db(
        conn=conn,
        student_id=student_id
    )


def delete_student_db(
        conn: psycopg2.connect,
        student_id: int
):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            DELETE FROM student
            WHERE id=(%s);
            """,
            (
                student_id,
            )
        )
        conn.commit()
