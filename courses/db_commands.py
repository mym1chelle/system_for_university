import psycopg2
from psycopg2.extras import NamedTupleCursor
from fastapi import status, HTTPException
from teachers.schemas import GetTeacherConfig
from teachers.db_commands import get_teacher_db
from courses.schemas import CreateCourseConfig, ResponseCourseConfig


def get_course_via_name(
        conn: psycopg2.connect,
        name: str
):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
                SELECT * FROM course
                WHERE name=(%s);
                """, (name,)
        )
        return cur.fetchone()


def add_course_db(
        conn: psycopg2.connect,
        course: CreateCourseConfig,
        teacher: GetTeacherConfig | None
):
    is_course_exist = get_course_via_name(conn=conn, name=course.curse_name)
    if is_course_exist:
        raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'The course already exist: {course.curse_name}'
            )
    else:
        course_programme_id = get_course_programme_db(
            conn=conn,
            course=course
        )
        course_teacher_id = get_teacher_db(
            conn=conn,
            teacher=teacher
        )
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO course (name, course_programme_id, teacher_id)
                VALUES (%s, %s, %s);
                """,
                (course.curse_name, course_programme_id, course_teacher_id)
            )
        conn.commit()
        return ResponseCourseConfig(
            curse_name=course.curse_name,
            course_programme_id=course_programme_id,
            teacher_id=course_teacher_id
        )


def get_course_programme_db(
        conn: psycopg2.connect,
        course: CreateCourseConfig
):
    name = course.course_programme_name
    if name:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(
                """
                SELECT id FROM course_programme
                WHERE name=(%s);
                """, (name,)
            )
            course_programme = cur.fetchone()
        if course_programme:
            return course_programme.id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'The course programme does not exist: {name}'
            )
    return name
