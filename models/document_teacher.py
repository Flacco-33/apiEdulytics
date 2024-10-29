from pydantic import BaseModel, Field
from typing import List, Dict

class RatingsAspects(BaseModel):
    positive: int
    negative: int

class SWOT(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

class TeacherEvaluationData(BaseModel):
    idTeacher: str
    idCourse: str
    SWOT: SWOT
    summaryComment: str
    ratingsAspects: Dict[str, RatingsAspects]
    teacherEvaluations: Dict[str, int]
    emotions: Dict[str, int]