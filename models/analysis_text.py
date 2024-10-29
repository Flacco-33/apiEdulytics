from typing import Optional
from pydantic import BaseModel

class DataAnalysisText(BaseModel):
    idCourse: str
    idTeacher: str
    idStudent: str
    aspect: int
    comment: str