from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from courses.schemas import CreateCourseConfig
from courses.db_commands import (
    add_course_db
)
from teachers.schemas import GetTeacherConfig


router = APIRouter(
    prefix='/courses',
    tags=['courses', ]
)


@router.post('')
async def add_course(
    course: CreateCourseConfig,
    teacher: GetTeacherConfig = None,
    conn=Depends(get_db_connection)
):
    """Добавление нового курса"""

    return add_course_db(
        conn=conn,
        course=course,
        teacher=teacher
    )
