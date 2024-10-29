from fastapi import APIRouter
from typing import List
from pymongo import MongoClient
from config.db import conn as db

from models.data_match import DataMatch as ResponseModel
from schemas.data_match import videoAnalysisEntity, textAnalysisEntity, matchEntity

dataMatch = APIRouter()

@dataMatch.get("/dataMatch",response_model=ResponseModel, tags=["DataMatch"], summary="Group data from video and text analysis")
def data_match():
    videos = list(db.analysis.videoAnalysis.find({}))
    texts = list(db.analysis.textAnalysis.find({}))
    
    matching = []
    ids_videos = []
    ids_texts = []

    formatted_videos = [videoAnalysisEntity(video) for video in videos]
    formatted_texts = [textAnalysisEntity(text) for text in texts]

    # Comparar los registros y construir la respuesta
    for video in formatted_videos:
        for text in formatted_texts:
            if (video["idStudent"] == text["idStudent"] and
                video["idTeacher"] == text["idTeacher"] and
                video["aspect"] == text["aspect"] and
                video["idCourse"] == text["idCourse"] and
                not video["analysed"] and not text["analysed"]):
                ids_videos.append(video["_id"])
                ids_texts.append(text["_id"])
                matching.append(matchEntity(video, text))
    
    print(len(matching))
    print(ids_videos)
    ResponseModel.dataMatch = matching
    return ResponseModel
