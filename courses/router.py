from fastapi import APIRouter, Depends
from typing import Optional
from data.db_config import get_db_connection
from courses.schemas import CreateCourseConfig
from courses.db_commands import (
    add_course_db,
    get_course_programme_db
)
from teachers.db_commands import get_teacher_db
from teachers.schemas import GetTeacherConfig


router = APIRouter(
    prefix='/courses',
    tags=['courses', ]
)


@router.post('')
async def add_course(
    course: CreateCourseConfig,
    teacher: Optional[GetTeacherConfig],
    conn=Depends(get_db_connection)
):
    """Добавление нового курса"""
    course_programme = get_course_programme_db(conn=conn, name=course.course_programme_name)
    print(course_programme)
    course_teacher = get_teacher_db(
        conn=conn,
        surname=teacher.surname,
        name=teacher.name,
        fathers_name=teacher.fathers_name
    )
    add_course_db(
        conn=conn,
        name=course.curse_name,
        course_programme_id=course_programme.id,
        teacher_id=course_teacher.id
    )