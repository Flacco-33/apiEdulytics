from pydantic import BaseModel, Field
from typing import List, Dict

class CommentInput(BaseModel):
    idStudent: str
    comment: str
    predominant_emotion: str

class SentimentInput(BaseModel):
    sentiment: str
    comments: List[CommentInput]

class AspectInput(BaseModel):
    aspect: int
    sentiments: Dict[str, List[CommentInput]]  # Diccionario de sentimientos con sus comentarios

class DocumentInput(BaseModel):
    idTeacher: str
    idCourse: str
    aspect: int
    sentiment: str
    comment: str
    predominant_emotion: str
    idStudent: str
