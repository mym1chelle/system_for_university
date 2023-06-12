from typing import List
from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from grades.schemas import AddNewGrade, ReturnNewGrade
from grades.db_commands import create_new_grade


router = APIRouter(
    prefix='/grades',
    tags=['grades', ]
)


@router.post('/add', response_model=ReturnNewGrade)
async def add_new_grade(
    new_grade: AddNewGrade,
    conn=Depends(get_db_connection)
):
    """Добавление нового варианта оценки"""
    return create_new_grade(
        conn=conn,
        grade_name=new_grade.grade
    )


@router.post('',)
async def add_new_grade_for_course(
    grade: AddNewGrade,
    conn=Depends(get_db_connection)
):
    """Добавляет оценку студенту за курс"""
    return create_new_grade(
        conn=conn,
        grade_name=new_grade.grade
    )