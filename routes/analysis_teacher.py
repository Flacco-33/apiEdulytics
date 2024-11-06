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

@analysisTeacher.get("/teacher_comments", response_model=List[TeacherComments], tags=["Teacher_comments"])
async def get_all_teacher_comments():
    """
    Asynchronously retrieves all teacher comments from the database and organizes them by aspects.
    
    Returns:
    
        List[TeacherComments]: A list of dictionaries containing teacher comments organized by aspects.
    
    Steps:
    
        1. Fetches all documents from the 'summaryAnalysis' collection in the database.
        2. Initializes an empty list to store the response.
        3. Iterates over each document fetched from the database.
        4. Filters the comments by aspects using the `get_comments_by_aspects` function.
        5. Constructs a response dictionary for each document with the teacher's ID, course ID, and aspects.
        6. Appends the constructed response to the response list.
        7. Returns the response list containing all teacher comments organized by aspects.
    
    """
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



@analysisTeacher.get("/evaluation/", response_model=TeacherEvaluationData , responses=responses, tags=["Get_evaluation"])
async def get_evaluation(idTeacher: str, idCourse: str):
    """
        Asynchronously retrieves the evaluation data for a specific teacher and course from the database.
        
        Args:
        
            idTeacher (str): The ID of the teacher.
            idCourse (str): The ID of the course.
        
        Returns:
        
            dict: The evaluation data if found, with the ObjectId converted to a string.
        
        Raises:
        
            HTTPException: If the evaluation is not found (404) or if an error occurs (500).
        
        Steps:
        
            1. Searches for the evaluation document in the database based on the teacher's ID and course ID.
            2. If the evaluation is found, converts the ObjectId to a string for JSON serialization.
            3. Returns the evaluation data.
            4. If the evaluation is not found, raises a 404 HTTPException.
            5. If any other error occurs, raises a 500 HTTPException with the error details.
    
    """
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
