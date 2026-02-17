"""
ASL Alphabet — Pydantic Schemas
================================
Request / response models shared across routers.
"""

from pydantic import BaseModel
from typing import List


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool



class Prediction(BaseModel):
    label: str
    confidence: float


class PredictionResponse(BaseModel):
    success: bool
    predictions: List[Prediction]
    top_label: str
    top_confidence: float