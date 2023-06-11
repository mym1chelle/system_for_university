from fastapi import FastAPI
from students.router import router as student_router
from teachers.router import router as teacher_router
from courses.router import router as course_router
# from grades.router import router as grade_router


app = FastAPI(
    debug=True,
    title='Системы управления университетом',
    description='API для cистемы управления университетом'
)

app.include_router(
    student_router
)

app.include_router(
    teacher_router
)

app.include_router(
    course_router
)

# app.include_router(
#     grade_router
# )
