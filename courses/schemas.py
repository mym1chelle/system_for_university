from typing import Optional
from pydantic import BaseModel
from teachers.schemas import GetTeacherFullInfo


class CourseProgrammeOptional(BaseModel):
    id: Optional[int]
    name: Optional[str]
    link_by_file: Optional[str]


class CreateCourse(BaseModel):
    curse_name: str
    course_programme_name: Optional[str]


class GetCourse(CreateCourse):
    pass


class CreateCourseResult(BaseModel):
    curse_name: str
    course_programme_id: int | None
    teacher_id: int | None


class GetCourseInfo(BaseModel):
    id: int
    name: str
    course_programme: CourseProgrammeOptional
    teacher: GetTeacherFullInfo


class GetCourseSmallInfo(BaseModel):
    id: int
    name: str
    course_programme_id: int | None
    teacher_id: int | None
