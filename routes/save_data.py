import json
from fastapi import APIRouter, HTTPException
from config.db import conn as db
from models.analysis_teacher import DocumentInput
from models.teacher_comments import TeacherComments
from models.document_teacher import TeacherEvaluationData
from bson import ObjectId
from typing import List

saveData = APIRouter()

@saveData.post("/storeDocument", tags=["Save_Data"]) 
async def store_document(data: DocumentInput):
    """
    Stores or updates a document in the MongoDB collection based on the provided data.
    
    **Args:**
    
        data (DocumentInput):The document data to be stored or updated.
            
    **Returns:**
    
        dict: A dictionary containing a message indicating whether the document was created or updated.
    """
    # Buscar si ya existe un documento con el idTeacher y idCourse
    existing_doc = db.analysis.summaryAnalysis.find_one({
        "idTeacher": data.idTeacher,
        "idCourse": data.idCourse
    })

    if existing_doc:
        # Buscar si ya existe el aspecto dentro de ese documento
        aspecto = next((asp for asp in existing_doc["aspectos"] if asp["aspect"] == data.aspect), None)
        
        if aspecto:
            # Verificar si el sentimiento ya existe en el aspecto
            if data.sentiment in aspecto["sentiments"]:
                # Si ya existe el sentimiento, agregar el nuevo comentario y emoción
                new_comment = {
                    "comment": data.comment,
                    "predominant_emotion": data.predominant_emotion
                }
                aspecto["sentiments"][data.sentiment].append(new_comment)
            else:
                # Si no existe el sentimiento, crearlo con el nuevo comentario
                aspecto["sentiments"][data.sentiment] = [{
                    "comment": data.comment,
                    "predominant_emotion": data.predominant_emotion
                }]
        else:
            # Si el aspecto no existe, crear un nuevo aspecto con su sentimiento
            new_aspecto = {
                "aspect": data.aspect,
                "sentiments": {
                    data.sentiment: [{
                        "comment": data.comment,
                        "predominant_emotion": data.predominant_emotion
                    }]
                }
            }
            existing_doc["aspectos"].append(new_aspecto)

        # Actualizar el documento en MongoDB
        db.analysis.summaryAnalysis.update_one(
            {"_id": existing_doc["_id"]},
            {"$set": {"aspectos": existing_doc["aspectos"]}}
        )
        return {"message": "Documento actualizado correctamente."}

    else:
        # Si no existe, crear un nuevo documento con el idTeacher, idCourse, aspecto, y sentimientos
        new_document = {
            "idTeacher": data.idTeacher,
            "idCourse": data.idCourse,
            "aspectos": [
                {
                    "aspect": data.aspect,
                    "sentiments": {
                        data.sentiment: [{
                            "comment": data.comment,
                            "predominant_emotion": data.predominant_emotion
                        }]
                    }
                }
            ]
        }
        db.analysis.summaryAnalysis.insert_one(new_document)
        return {"message": "Documento creado correctamente."}



@saveData.post("/saveEvaluation", tags=["Save_Data"])
async def save_evaluation(data: TeacherEvaluationData):
    """
    Saves a teacher evaluation to the MongoDB database.
    
    **Args:**
        
        - data (TeacherEvaluationData): The teacher evaluation data to be saved.
    
    **Returns:**
         
        - dict: A dictionary containing a success message and the ID of the inserted document.
    
    **Raises:**
         
        - HTTPException: If an error occurs while saving the evaluation.
    """
    try:
        # Convertir el objeto Pydantic a un diccionario
        evaluation_data = data.model_dump()

        # Insertar el diccionario en la colección de MongoDB
        result = db.analysis.resultEvaluation.insert_one(evaluation_data)
        return {"message": "Evaluation saved successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")