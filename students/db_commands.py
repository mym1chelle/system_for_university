import psycopg2
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException
from students.schemas import StudentInfoForCreation, StudentInfoOptional


def get_group_id_by_code(conn: psycopg2.connect, group_code: int):
    """
    Выводит данные группы по коду группы
    Если группы с таким кодом не найдено — вызовет ошибку 404
    """
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            "SELECT id FROM students_group WHERE code=(%s);",
            (group_code,)
        )
        group = cur.fetchone()
        if group:
            return group
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The group with code «{group_code}» does not exist'
            )


def get_student_by_id_or_404(conn: psycopg2.connect, student_id: int):
    """
    Выводит информациб о студенте по ID
    если студент с таким ID не был найден — вызовет ошибку 404
    """
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
        student = cur.fetchone()
        if student:
            return {
                'id': student.id,
                'surname': student.surname,
                'name': student.name,
                'fathers_name': student.fathers_name,
                'date_of_birth': student.date_of_birth,
                'group_code': student.code
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The student with ID «{student_id}» does not exist'
            )


def add_new_student(
        conn: psycopg2.connect,
        student: StudentInfoForCreation
):
    """
    Добавляет запись о новом студенте в БД

    Производит проверки на существование всех необходимых
    данных для добавления записи в БД и производит валидацию
    """
    group_id = get_group_id_by_code(conn=conn, group_code=student.group_code)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO student (
                surname, name, fathers_name, date_of_birth, group_id
            ) VALUES (%s, %s, %s, %s, %s);
            """,
            (
                student.surname,
                student.name,
                student.fathers_name,
                student.date_of_birth,
                group_id
            )
        )
    conn.commit()
    return {
        'surname': student.surname,
        'name': student.name,
        'fathers_name': student.fathers_name,
        'date_of_birth': student.date_of_birth,
        'group_code': student.group_code
    }


def update_student(
        conn: psycopg2.connect,
        student: StudentInfoOptional,
        student_id: int
):
    """
    Изменяет данные студента в БД

    Производит проверки на существование всех необходимых
    данных для изменения записи в БД и производит валидацию
    """

    if student.group_code is not None:
        group = get_group_id_by_code(
            conn=conn, group_code=student.group_code
        )
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
                    student.surname,
                    student.name,
                    student.fathers_name,
                    student.date_of_birth,
                    group.id,
                    student_id,
                )
            )
        conn.commit()
    else:
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
                    student.surname,
                    student.name,
                    student.fathers_name,
                    student.date_of_birth,
                    student.group_code,
                    student_id,
                )
            )
        conn.commit()
    return {
        'id': student_id,
        'surname': student.surname,
        'name': student.name,
        'fathers_name': student.fathers_name,
        'date_of_birth': student.date_of_birth,
        'group_code': student.group_code
    }


def delete_student_db(
        conn: psycopg2.connect,
        student_id: int
):
    """
    Удаляет студента из базы данных
    """
    get_student_by_id_or_404(conn=conn, student_id=student_id)
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
    return {"detail": f"Student with ID «{student_id}» was delete"}
