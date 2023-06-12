from typing import Optional
from pydantic import BaseModel


class AddNewGrade(BaseModel):
    grade: str


class ReturnNewGrade(BaseModel):
    id: int
    grade: str
