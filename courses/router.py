from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from courses.schemas import CreateCourse, GetCourseInfo
from courses.db_commands import (
    add_course_db,
    get_course_by_id
)
from teachers.schemas import GetTeacher


router = APIRouter(
    prefix='/courses',
    tags=['courses', ]
)


@router.post('')
async def add_course(
    course: CreateCourse,
    teacher: GetTeacher = None,
    conn=Depends(get_db_connection)
):
    """Добавление нового курса"""

    return add_course_db(
        conn=conn,
        course=course,
        teacher=teacher
    )


@router.get('/{course_id}', response_model=GetCourseInfo)
async def get_course(
    course_id: int,
    conn=Depends(get_db_connection)
):
    """Вывод информации о курсе по ID"""

    course = get_course_by_id(
        conn=conn,
        id=course_id
    )
    return course