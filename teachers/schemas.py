from typing import Optional
from pydantic import BaseModel


class GetTeacherConfig(BaseModel):
    id: int
    surname: str
    name: str
    fathers_name: Optional[str]
