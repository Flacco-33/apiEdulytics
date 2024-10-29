from typing import Dict, List
from pydantic import BaseModel

class VideoEmotions(BaseModel):
    happy: float
    sad: float
    anger: float
    surprise: float
    neutral: float
    disgust: float
    fear: float
    contempt: float

class TextEmotions(BaseModel):
    happy: float
    sad: float
    anger: float
    surprise: float
    neutral: float
    disgust: float
    fear: float
    contempt: float

class VideoAnalysis(BaseModel):
    emotions: VideoEmotions

class TextAnalysis(BaseModel):
    comment: str
    emotions: TextEmotions
    sentiment: str

class Data(BaseModel):
    idStudent: str  
    idTeacher: str  
    aspect: int
    idCourse: str
    video_analysis: VideoAnalysis
    text_analysis: TextAnalysis

class DataMatch(BaseModel):
    dataMatch: List[Data]
