from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from courses.schemas import CreateCourseConfig
from courses.db_commands import (
    add_course_db,
    get_course_via_id
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


@router.get('/{course_id}')
async def get_course(
    course_id: int,
    conn=Depends(get_db_connection)
):
    """Вывод информации о курсе по ID"""

    return get_course_via_id(
        conn=conn,
        id=course_id
    )
