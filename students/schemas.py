from typing import Optional
from pydantic import BaseModel
from datetime import date


class CreateStudent(BaseModel):
    surname: str
    name: str
    fathers_name: Optional[str]
    date_of_birth: date
    group_code: Optional[int]


class GetStudent(BaseModel):
    id: int
    surname: str
    name: str
    fathers_name: Optional[str] | None
    date_of_birth: date
    group_code: Optional[int] | None


class ChangeStudent(BaseModel):
    surname: Optional[str]
    name: Optional[str]
    fathers_name: Optional[str]
    date_of_birth: Optional[date]
    group_code: Optional[int]
