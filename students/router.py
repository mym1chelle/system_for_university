from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from students.schemas import (
    StudentInfoForCreation,
    StudentInfo,
    StudentInfoOptional
)
from students.db_commands import (
    add_student_db,
    get_student_by_id_or_404,
    update_student,
    delete_student_db
)


router = APIRouter(
    prefix='/students',
    tags=['students', ]
)


@router.post('', response_model=StudentInfoForCreation)
async def add_student(
    student: StudentInfoForCreation,
    conn=Depends(get_db_connection)
):
    """Добавление нового студента"""
    return add_student_db(
        conn=conn,
        student=student
    )


@router.get('/{student_id}', response_model=StudentInfo)
async def get_student(
    student_id: int,
    conn=Depends(get_db_connection)
):
    """Выбор студента по ID"""
    return get_student_by_id_or_404(conn=conn, student_id=student_id)


@router.put('/{student_id}', response_model=StudentInfo)
async def edit_student(
    student_id: int,
    student: StudentInfoOptional,
    conn=Depends(get_db_connection)
):
    """Изменить данные студента по ID"""
    s = update_student(
        conn=conn,
        student=student,
        student_id=student_id
    )
    print(s)
    return s


@router.delete('/{student_id}')
async def delete_student(
    student_id: int,
    conn=Depends(get_db_connection)
):
    """Удалить студента по ID"""
    return delete_student_db(conn=conn, student_id=student_id)
