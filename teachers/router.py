from typing import List
from fastapi import APIRouter, Depends
from data.db_config import get_db_connection
from teachers.db_commands import get_all_teachers_db
from teachers.schemas import TeacherFullInfo


router = APIRouter(
    prefix='/teachers',
    tags=['teachers', ]
)


@router.get('', response_model=List[TeacherFullInfo])
async def get_all_teachers(
    conn=Depends(get_db_connection),
    limit: int = 15,
    offset: int = 0,
):
    """Показывает всех преподавателей"""
    return get_all_teachers_db(
        conn=conn,
        limit=limit,
        offset=offset
    )
