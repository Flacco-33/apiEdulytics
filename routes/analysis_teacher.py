import json
from fastapi import APIRouter, HTTPException
from config.db import conn as db
from models.analysis_teacher import DocumentInput
from models.teacher_comments import TeacherComments
from models.document_teacher import TeacherEvaluationData
from bson import ObjectId
from typing import List

analysisTeacher = APIRouter()

responses = {
    404: {"description": "Evaluation not found"},
    500: {"description": "An error occurred"}
}


def get_comments_by_aspects(document):
    aspects_list = []
    for aspecto in document["aspectos"]:
        positive_comments = aspecto["sentiments"].get("positive", [])
        negative_comments = aspecto["sentiments"].get("negative", [])

        aspects_list.append({
            "aspect": aspecto["aspect"],
            "positive_comments": positive_comments,
            "negative_comments": negative_comments,
            "positive_count": len(positive_comments),
            "negative_count": len(negative_comments),
        })
    
    return aspects_list

@analysisTeacher.get("/teacher_comments", response_model=List[TeacherComments], tags=["teacher_comments"])
async def get_all_teacher_comments():
    # Busca todos los documentos en la colección
    documents = db.analysis.summaryAnalysis.find()
    
    response_list = []
    
    for document in documents:
        # Filtra los comentarios por aspecto
        aspects = get_comments_by_aspects(document)
        
        # Construye la respuesta para cada documento
        response = {
            "idTeacher": document["idTeacher"],
            "idCourse": document["idCourse"],
            "aspects": aspects
        }
        
        response_list.append(response)
    
    return response_list



# Endpoint para buscar un documento por iddocente y idmateria
@analysisTeacher.get("/evaluation/", response_model=TeacherEvaluationData , responses=responses)
async def get_evaluation(idTeacher: str, idCourse: str):
    try:
        # Buscar el documento en la colección basado en iddocente e idmateria
        evaluation = db.analysis.resultEvaluation.find_one({"idTeacher": idTeacher, "idCourse": idCourse})

        if evaluation:
            # Convertir ObjectId a string para que sea serializable en JSON
            evaluation["_id"] = str(evaluation["_id"])
            return evaluation
        else:
            raise HTTPException(status_code=404, detail="Evaluation not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
