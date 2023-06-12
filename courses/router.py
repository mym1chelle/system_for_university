from typing import List
from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from courses.schemas import CreateCourse, GetCourseInfo
from courses.db_commands import (
    add_course_db,
    get_course_by_id,
    get_all_sudents_in_course
)
from students.schemas import GetAllStudentsInCourse


router = APIRouter(
    prefix='/courses',
    tags=['courses', ]
)


@router.post('', response_model=GetCourseInfo)
async def add_course(
    course: CreateCourse,
    teacher_id: int | None,
    conn=Depends(get_db_connection)
):
    """Добавление нового курса"""

    return add_course_db(
        conn=conn,
        course=course,
        teacher_id=teacher_id
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


@router.get('/{course_id}/students', response_model=List[GetAllStudentsInCourse])
async def get_students_in_courser(
    course_id: int,
    conn=Depends(get_db_connection),
    limit: int = 15,
    offset: int = 0,
):
    """Вывод всех студентов, которые обучаются на курсе"""
    return get_all_sudents_in_course(
        conn=conn,
        course_id=course_id,
        limit=limit,
        offset=offset
    )
