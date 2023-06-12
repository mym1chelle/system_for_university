from typing import Optional
from pydantic import BaseModel


class TeacherFullInfo(BaseModel):
    id: int
    surname: str
    name: str
    fathers_name: str | None


class TeacherFullInfoOptional(BaseModel):
    id: Optional[int]
    surname: Optional[str]
    name: Optional[str]
    fathers_name: Optional[str]


class TeacherID(BaseModel):
    id: int | None
