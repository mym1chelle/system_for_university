from fastapi import APIRouter, Depends
from fastapi import status, HTTPException
from psycopg2.extras import NamedTupleCursor
from data.db_config import get_db_connection
from students.schemas import CreateStudentConfig, GetStudentConfig


router = APIRouter(
    prefix='/students',
    tags=['students', ]
)


@router.post('/', response_model=CreateStudentConfig)
async def add_student(
    student: CreateStudentConfig,
    conn=Depends(get_db_connection)
):
    """Добавление нового студента"""
    group_id = None
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            "SELECT id FROM students_group WHERE code=(%s);",
            (student.group_code,)
        )
        group = cur.fetchone()
    if group:
        group_id = group.id
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO student (
                surname, name, fathers_name, date_of_birth, group_id
            ) VALUES (%s, %s, %s, %s, %s);""",
            (
                student.surname,
                student.name,
                student.fathers_name,
                student.date_of_birth,
                group_id
            )
        )
    conn.commit()
    return student


@router.get('/{student_id}')
async def get_student(
    student_id: int,
    conn=Depends(get_db_connection)
):
    """Выбор студента по ID"""
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            """
            SELECT st.id, st.name, st.surname, st.fathers_name, st.date_of_birth, gp.code
            FROM student as st
            LEFT JOIN students_group as gp ON gp.id=st.group_id
            WHERE st.id=(%s)
            ;
            """,
            (student_id,)
        )
        student = cur.fetchone()
        print(student)
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