import psycopg2
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException
from grades.schemas import GradeForCourseInfoForCreation
from students.db_commands import get_student_by_id_or_404
from courses.db_commands import get_course_by_id_or_404


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


def get_grade_by_name_or_404(
        conn: psycopg2.connect,
        grade_name: str
):
    grade = get_grade_by_name(
        conn=conn,
        grade_name=grade_name
    )
    if not grade:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The grade «{grade_name}» does not exist'
            )
    else:
        return {
            'id': grade.id,
            'grade': grade.grade
        }


def create_new_grade(
        conn: psycopg2.connect,
        grade_name: str
):
    grade = get_grade_by_name(conn=conn, grade_name=grade_name)
    if grade:
        raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'The grade «{grade_name}» already exists'
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


def grade_not_exists_or_404(
        conn: psycopg2.connect,
        course_id: int,
        student_id: int
):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            SELECT * FROM course_grade
            WHERE course_id=(%s) AND student_id=(%s);
            """,
            (course_id, student_id)
        )
        grade = cur.fetchone()
    if grade:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='The grade for this student in this course already exists'
        )
    else:
        return None


def add_new_grade_for_course(
        conn: psycopg2.connect,
        data_for_grade: GradeForCourseInfoForCreation
):
    grade = get_grade_by_name_or_404(
        conn=conn,
        grade_name=data_for_grade.grade
    )
    student = get_student_by_id_or_404(
        conn=conn,
        student_id=data_for_grade.student_id
    )
    course = get_course_by_id_or_404(
        conn=conn,
        id=data_for_grade.course_id
    )
    is_grade_exists = grade_not_exists_or_404(
        conn=conn,
        course_id=data_for_grade.course_id,
        student_id=data_for_grade.student_id
    )
    if not is_grade_exists:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO course_grade (student_id, course_id, grade_id)
                VALUES (%s, %s, %s);
                """,
                (student.get('id'), course.get('id'), grade.get(id))
            )
            conn.commit()
        return {
            'student': student,
            'course': course,
            'grade': grade
        }


def get_grade_for_course_data_or_404(
        conn: psycopg2.connect,
        id: int
):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            SELECT * FROM course_grade
            WHERE id=(%s);
            """,
            (id,)
        )
        grade_for_course = cur.fetchone()
        if not grade_for_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The grade for course with ID «{id}» does not exist'
            )
        else:
            return grade_for_course


def edit_grade_for_course(
        conn: psycopg2.connect,
        grade_name: str,
        course_grade_id: int
):
    grade = get_grade_by_name_or_404(
        conn=conn,
        grade_name=grade_name
    )
    grade_for_course = get_grade_for_course_data_or_404(
        conn=conn,
        id=course_grade_id
    )
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            UPDATE course_grade SET
                grade_id=(%s)
            WHERE id=(%s);
            """,
            (
                grade.get('id'),
                grade_for_course.id
            )
        )
        conn.commit()
        return {
            'id': grade_for_course.id,
            'student_id': grade_for_course.student_id,
            'course_id': grade_for_course.course_id,
            'grade_id': grade.get('id')
        }
