from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from grades.schemas import (
    GradeForEdit,
    GradeNameForCreation,
    GradeInfo,
    GradeForCourseInfoForCreation,
    GradeInfoAfterCreate,
    GradeForCourseInfoAfterUpdate
)
from grades.db_commands import (
    create_new_grade,
    add_new_grade_for_course,
    edit_grade_for_course
)


router = APIRouter(
    prefix='/grades',
    tags=['grades', ]
)


@router.post('/add', response_model=GradeInfo)
async def add_new_grade(
    new_grade: GradeNameForCreation,
    conn=Depends(get_db_connection)
):
    """Добавление нового варианта оценки"""
    return create_new_grade(
        conn=conn,
        grade_name=new_grade.grade
    )


@router.post('', response_model=GradeInfoAfterCreate)
async def add_new_grade_for_course_by_student(
    data_for_grade: GradeForCourseInfoForCreation,
    conn=Depends(get_db_connection)
):
    """Добавление оценки студенту за курс"""
    return add_new_grade_for_course(
        conn=conn,
        data_for_grade=data_for_grade
    )


@router.put('/{grade_id}', response_model=GradeForCourseInfoAfterUpdate)
async def update_grade_for_course_by_student(
    data_for_grade: GradeForEdit,
    grade_id: int,
    conn=Depends(get_db_connection)
):
    """Обновление оценки студента за курс"""
    return edit_grade_for_course(
        conn=conn,
        grade_name=data_for_grade.grade,
        course_grade_id=grade_id
    )
