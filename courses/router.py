from typing import List
from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from courses.schemas import CreateCourse, CourseInfo
from courses.db_commands import (
    add_new_course,
    get_course_by_id_or_404,
    get_all_sudents_in_course
)
from students.schemas import StudentInfo
from teachers.schemas import TeacherID


router = APIRouter(
    prefix='/courses',
    tags=['courses', ]
)


@router.post('', response_model=CourseInfo)
async def add_course(
    course: CreateCourse,
    teacher: TeacherID | None = None,
    conn=Depends(get_db_connection)
):
    """Добавление нового курса"""

    return add_new_course(
        conn=conn,
        course=course,
        teacher=teacher
    )


@router.get('/{course_id}', response_model=CourseInfo)
async def get_course(
    course_id: int,
    conn=Depends(get_db_connection)
):
    """Вывод информации о курсе по ID"""

    course = get_course_by_id_or_404(
        conn=conn,
        id=course_id
    )
    return course


@router.get('/{course_id}/students', response_model=List[StudentInfo])
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
