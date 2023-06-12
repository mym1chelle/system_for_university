from typing import List
from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from teachers.db_commands import get_all_teachers_db
from teachers.schemas import GetAllTeachers


router = APIRouter(
    prefix='/teachers',
    tags=['teachers', ]
)


@router.get('', response_model=List[GetAllTeachers])
async def get_all_teachers(
    conn=Depends(get_db_connection),
    limit: int = 15,
    offset: int = 0,
):
    """Вывод всех преподавателей"""
    return get_all_teachers_db(
        conn=conn,
        limit=limit,
        offset=offset
    )
