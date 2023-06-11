from typing import Optional
from pydantic import BaseModel
from datetime import date


class CreateStudentConfig(BaseModel):
    surname: str
    name: str
    fathers_name: Optional[str]
    date_of_birth: date
    group_code: Optional[int]


class GetStudentConfig(BaseModel):
    id: int
    surname: str
    name: str
    fathers_name: Optional[str]
    date_of_birth: date
    group_code: Optional[int]


class ChangeStudentConfig(BaseModel):
    surname: Optional[str]
    name: Optional[str]
    fathers_name: Optional[str]
    date_of_birth: Optional[date]
    group_code: Optional[int]
