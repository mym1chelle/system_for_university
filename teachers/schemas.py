from typing import Optional
from pydantic import BaseModel


class GetAllTeachers(BaseModel):
    id: int
    surname: str
    name: str
    fathers_name: Optional[str]


class GetTeacherFullInfo(BaseModel):
    id: Optional[int]
    surname: Optional[str]
    name: Optional[str]
    fathers_name: Optional[str]


class GetTeacher(BaseModel):
    surname: Optional[str]
    name: Optional[str]
    fathers_name: Optional[str]
