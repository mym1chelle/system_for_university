from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from students.schemas import (
    CreateStudentConfig,
    GetStudentConfig,
    ChangeStudentConfig
)
from students.db_commands import (
    get_group_via_code_db,
    add_student_db,
    get_student_db,
    edit_student_db,
    delete_student_db
)


router = APIRouter(
    prefix='/students',
    tags=['students', ]
)


@router.post('/')
async def add_student(
    student: CreateStudentConfig,
    conn=Depends(get_db_connection)
):
    """Добавление нового студента"""
    group = get_group_via_code_db(conn=conn, group_code=student.group_code)
    group_id = group.id if group else None
    group_code = group.code if group else None
    add_student_db(
        conn=conn,
        surname=student.surname,
        name=student.name,
        fathers_name=student.fathers_name,
        date_of_birth=student.date_of_birth,
        group_id=group_id
    )
    return CreateStudentConfig(**{
        'surname': student.surname,
        'name': student.name,
        'fathers_name': student.fathers_name,
        'date_of_birth': student.date_of_birth,
        'group_code': group_code
    })


@router.get('/{student_id}')
async def get_student(
    student_id: int,
    conn=Depends(get_db_connection)
):
    """Выбор студента по ID"""
    student = get_student_db(conn=conn, student_id=student_id)
    if student:
        return GetStudentConfig(**{
            'id': student.id,
            'surname': student.surname,
            'name': student.name,
            'fathers_name': student.fathers_name,
            'date_of_birth': student.date_of_birth,
            'group_code': student.code
        })
    return {}


@router.put('/{student_id}')
async def edit_student(
    student_id: int,
    student: ChangeStudentConfig,
    conn=Depends(get_db_connection)
):
    """Изменить данные студента по ID"""
    changed_student = edit_student_db(
        conn=conn,
        surname=student.surname,
        name=student.name,
        fathers_name=student.fathers_name,
        date_of_birth=student.date_of_birth,
        group_code=student.group_code,
        student_id=student_id
    )
    return GetStudentConfig(**{
        'id': changed_student.id,
        'surname': changed_student.surname,
        'name': changed_student.name,
        'fathers_name': changed_student.fathers_name,
        'date_of_birth': changed_student.date_of_birth,
        'group_code': student.group_code
    })


@router.delete('/{student_id}')
async def delete_student(
    student_id: int,
    conn=Depends(get_db_connection)
):
    """Изменить данные студента по ID"""
    delete_student_db(conn=conn, student_id=student_id)
    return {}
