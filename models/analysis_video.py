from typing import Optional
from pydantic import BaseModel

class DataAnalysisVideo(BaseModel):
    idCourse: str
    idTeacher: str
    idStudent: str
    aspect: int
    video_url: str