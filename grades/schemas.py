from pydantic import BaseModel
from courses.schemas import GetCourseSmallInfo
from students.schemas import GetStudentSmallInfo


class AddNewGrade(BaseModel):
    grade: str


class ReturnNewGrade(BaseModel):
    id: int
    grade: str


class AddNewGradeForCourse(BaseModel):
    grade: str
    student_id: int
    course_id: int


class GradeInfoAfterCreate(BaseModel):
    student: GetStudentSmallInfo
    course: GetCourseSmallInfo
    grade: ReturnNewGrade