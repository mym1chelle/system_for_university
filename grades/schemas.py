from pydantic import BaseModel
from courses.schemas import CourseSmallInfo
from students.schemas import StudentSmallInfo


class GradeNameForCreation(BaseModel):
    grade: str


class GradeForEdit(GradeNameForCreation):
    pass


class GradeInfo(BaseModel):
    id: int
    grade: str


class GradeForCourseInfoForCreation(BaseModel):
    grade: str
    student_id: int
    course_id: int


class GradeInfoAfterCreate(BaseModel):
    student: StudentSmallInfo
    course: CourseSmallInfo
    grade: GradeInfo


class GradeForCourseInfoAfterUpdate(BaseModel):
    id: int
    student_id: int
    course_id: int
    grade_id: int
