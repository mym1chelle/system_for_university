from typing import Optional
from pydantic import BaseModel


class CreateCourseConfig(BaseModel):
    curse_name: str
    course_programme_name: Optional[str]
