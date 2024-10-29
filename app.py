from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#import routes
from routes.user import user as user_router
from routes.analysis import analysis as analysis_router
from routes.data_match import dataMatch as data_Match_router
from routes.analysis_teacher import analysisTeacher as analysis_teacher_router
from routes.save_data import saveData as save_data_router
#import docuemntation tags
from docs import tags_metadata

app = FastAPI(
    title="FastAPI MongoDB",
    description="This is a simple example of a FastAPI application with MongoDB.",
    version="0.1.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a los dominios específicos que desees, como ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Esto permite todos los métodos (GET, POST, PUT, DELETE, etc.), o puedes especificar ['POST']
    allow_headers=["*"],  # Esto permite todos los encabezados, puedes restringirlo a los necesarios
)

app.include_router(user_router)
app.include_router(analysis_router)
app.include_router(data_Match_router)
app.include_router(analysis_teacher_router)
app.include_router(save_data_router)
