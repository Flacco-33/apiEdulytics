from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Response, status


class responseAnalysis(BaseModel):
    message: str