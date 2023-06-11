from typing import Optional
from pydantic import BaseModel


class CreateCourseConfig(BaseModel):
    curse_name: str
    course_programme_name: Optional[str]


class ResponseCourseConfig(BaseModel):
    curse_name: str
    course_programme_id: int | None
    teacher_id: int | None
