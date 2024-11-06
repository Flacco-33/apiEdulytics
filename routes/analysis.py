import json
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from config.db import conn as db
from models.analysis_video import DataAnalysisVideo as AnalisisModelVideo
from models.analysis_text import DataAnalysisText as AnalysisModelText
from models.response_analysis import responseAnalysis as ResponseModel 
from bson import ObjectId
import asyncio
import os
from gradio_client import Client
import httpx
from dotenv import load_dotenv

load_dotenv()

analysis = APIRouter()

responses = {
    503: {"description": "The server is not available"}
}

url_video = os.getenv('URL_VIDEO')
url_text = os.getenv('URL_TEXT')
url_analysis = os.getenv('URL_ANALYSIS')

async def process_data_video(analisis:AnalisisModelVideo):
    """
    Asynchronously processes video analysis data and stores the result in the database.
    Args:
        analisis (AnalisisModelVideo): The analysis model containing video data.
    Returns:
        None
    Steps:
        1. Converts the analysis model to a dictionary.
        2. Extracts the video URL from the dictionary.
        3. Sends a prediction request to the client with the video URL.
        4. Parses the prediction result from JSON.
        5. Prepares the data to be stored in the database.
        6. Inserts the data into the video analysis collection.
        7. Retrieves and prints the inserted document from the database.
    """
    anlisysData = dict(analisis)
    url = anlisysData["video_url"]
    client = Client(url_video)
    result = client.predict(
    		video_url=url,
    		api_name="/predict"
    )
    print(result)
    print(anlisysData)
    
    data_to_store = {
    'result': result,
    'data': anlisysData,
    'analysed': False
    }
    id = db.analysis.videoAnalysis.insert_one(data_to_store).inserted_id
    # Recuperar el documento con el ID insertado
    video_analysis = db.analysis.videoAnalysis.find_one({"_id": ObjectId(id)})
    print(video_analysis)
    pass

@analysis.post('/videoAnalysis', response_model=ResponseModel, responses=responses, tags=["Analysis"] ,summary="Video analysis")
async def video_analysis(analisis:AnalisisModelVideo):
    """
    **Endpoint to handle video analysis requests.**

    This endpoint receives video analysis data, processes it asynchronously, and returns a confirmation message.

    **Args:**
        
        analisis (AnalisisModelVideo): The video analysis data model.

    **Returns:**
        
        dict: A dictionary containing a confirmation message .
    """
    url = url_video
    try:
        is_server_alive = await check_server_health(url)
        if not is_server_alive:
            return JSONResponse(
                content={"message": "The video analysis server is not available."},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        asyncio.create_task(process_data_video(analisis))
        return ResponseModel(message="Datos recibidos")
    except Exception as e:
            return ({ "error": str(e) })
        
"""
    Text analysis
"""
async def process_data_text(analisis:AnalysisModelText):
    """
    Asynchronously processes text analysis data and stores the result in the database.
    Args:
        analisis (AnalysisModelText): The analysis model containing text data.
    Returns:
        None
    Steps:
        1. Converts the analysis model to a dictionary.
        2. Extracts the comment from the dictionary.
        3. Sends a prediction request to the client with the comment.
        4. Prepares the data to be stored in the database.
        5. Inserts the data into the text analysis collection.
        6. Retrieves and prints the inserted document from the database.
    """
    anlisysData = dict(analisis)
    comment = anlisysData["comment"]
    client = Client(url_text)
    result = client.predict(
    		comment=comment,
    		api_name="//analyze_comment"
    )
    json_result = json.loads(result)
    print(json_result)
    data_to_store = {
    'result': json_result,
    'data': anlisysData,
    'analysed': False
    }
    id = db.analysis.textAnalysis.insert_one(data_to_store).inserted_id
    # Recuperar el documento con el ID insertado
    text_analysis = db.analysis.textAnalysis.find_one({"_id": ObjectId(id)})
    print(text_analysis)
    pass
        
@analysis.post('/textAnalysis', response_model=ResponseModel,responses=responses, tags=["Analysis"], summary="Text analysis")
async def text_analysis(analisis:AnalysisModelText):
    """
    **Endpoint to handle text analysis requests.**
    
    This endpoint receives text analysis data, processes it asynchronously, and returns a confirmation message.
    
    **Args:**
        
        analisis (AnalysisModelText): The text analysis data model.
    
    **Returns:**
        
        dict: A dictionary containing a confirmation message or an error message.
    
    """
    try:
        url = url_text
        is_server_alive = await check_server_health(url)
        if not is_server_alive:
            return JSONResponse(
                content={"message": "The text analysis server is not available."},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        asyncio.create_task(process_data_text(analisis))
        return ResponseModel(message="Datos recibidos")
    except Exception as e:
            return ({ "error": str(e) })
    

"""
    Analysis Data
"""
async def process_analysis_data():
    """
    Asynchronously processes analysis data by sending a request to an analysis API.
    This function creates a client instance with the specified analysis URL, sends a prediction request
    to the API endpoint "//analyze_comment", and prints the result.
    """
   
    client = Client(url_analysis)
    result = client.predict(
    		api_name="//combined_analysis"
    )
    print(result)
    pass
        
@analysis.post('/analysisData', response_model=ResponseModel,responses=responses, tags=["Analysis_data"], summary="Analysis data")
async def analysis_data():
    """
    Endpoint to perform text analysis.

    This endpoint receives a request to analyze text data and processes it asynchronously.
    It first checks if the text analysis server is available. If the server is not available,
    it returns a 503 Service Unavailable response. If the server is available, it creates
    an asynchronous task to process the analysis data and returns a response indicating
    that the data has been received.

    Returns:
    
        JSONResponse: A response indicating the status of the text analysis request.
    
    """
    try:
        url = url_analysis
        is_server_alive = await check_server_health(url)
        if not is_server_alive:
            return JSONResponse(
                content={"message": "The text analysis server is not available."},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        asyncio.create_task(process_analysis_data())
        return ResponseModel(message="Datos recibidos")
    except Exception as e:
            return ({ "error": str(e) })


async def check_server_health(server_url: str) -> bool:
    """
    Check if the server is alive by sending a simple GET request.
    Args:
        server_url (str): The server URL to check.
    Returns:
        bool: True if the server responds with a status code 200, False otherwise.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(server_url)
            if response.status_code == 200:
                return True
            return False
    except httpx.RequestError as e:
        print(f"Error checking server health: {e}")
        return False
