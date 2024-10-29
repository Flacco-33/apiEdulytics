from typing import Optional, List, Dict
from pydantic import BaseModel

class AspectComments(BaseModel):
    aspect: int
    positive_comments: List[Dict]
    negative_comments: List[Dict]
    positive_count: int
    negative_count: int

class TeacherComments(BaseModel):
    idTeacher: str
    idCourse: str
    aspects: List[AspectComments]