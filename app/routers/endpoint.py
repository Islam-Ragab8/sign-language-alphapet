"""
ASL Alphabet — API Endpoints
"""
import os, io
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schema.schema import Prediction, PredictionResponse, HealthResponse

router = APIRouter()

BASE_DIR         = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KERAS_MODEL_PATH = os.path.join(BASE_DIR, "models", "asl_resnet50_final.keras")
IMAGE_SIZE       = 224

model = None
class_names = None


def load_keras_model():
    global model, class_names
    model = load_model(KERAS_MODEL_PATH)
    class_names = [chr(i) for i in range(65, 91)] + ["del", "nothing", "space"]


@router.get("/health", response_model=HealthResponse, tags=["Utility"])
async def health_check():
    return HealthResponse(status="healthy", model_loaded=model is not None)



@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(file: UploadFile = File(...)):
    """Upload an image → top-5 ASL predictions."""
    if model is None:
        raise HTTPException(503, "Model not loaded.")
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image.")

    try:
        img = Image.open(io.BytesIO(await file.read())).convert("RGB")
        img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
        arr = preprocess_input(np.expand_dims(np.array(img, dtype=np.float32), 0))

        preds = model.predict(arr, verbose=0)[0]
        top5  = np.argsort(preds)[::-1][:5]

        results = [
            Prediction(label=class_names[i], confidence=round(float(preds[i]) * 100, 2))
            for i in top5
        ]
        return PredictionResponse(
            success=True, predictions=results,
            top_label=results[0].label, top_confidence=results[0].confidence,
        )
    except Exception as e:
        raise HTTPException(500, f"Prediction failed: {e}")
