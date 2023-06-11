from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from teachers.db_commands import get_all_teachers_db
from teachers.schemas import GetAllTeachersConfig


router = APIRouter(
    prefix='/teachers',
    tags=['teachers', ]
)


@router.get('')
async def get_all_teachers(
    conn=Depends(get_db_connection),
    limit: int = 15,
    offset: int = 0,
):
    """Вывод всех преподавателей"""
    teachers = get_all_teachers_db(
        conn=conn,
        limit=limit,
        offset=offset
    )
    return [
        GetAllTeachersConfig(
            id=teacher.id,
            surname=teacher.surname,
            name=teacher.name,
            fathers_name=teacher.fathers_name
        ) for teacher in teachers
    ]
