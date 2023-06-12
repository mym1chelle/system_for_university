from typing import Optional
from pydantic import BaseModel
from teachers.schemas import TeacherFullInfoOptional


class CourseProgrammeOptional(BaseModel):
    id: Optional[int]
    name: Optional[str]
    link_by_file: Optional[str]


class CreateCourse(BaseModel):
    curse_name: str
    course_programme_name: Optional[str]


class CourseData(CreateCourse):
    pass


class CourseInfo(BaseModel):
    id: int
    name: str
    course_programme: CourseProgrammeOptional
    teacher: TeacherFullInfoOptional


class CourseSmallInfo(BaseModel):
    id: int
    name: str
    course_programme_id: int | None
    teacher_id: int | None
