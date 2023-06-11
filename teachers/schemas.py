from typing import Optional
from pydantic import BaseModel


class GetAllTeachersConfig(BaseModel):
    id: int
    surname: str
    name: str
    fathers_name: Optional[str]


class GetTeacherConfig(BaseModel):
    surname: Optional[str]
    name: Optional[str]
    fathers_name: Optional[str]
