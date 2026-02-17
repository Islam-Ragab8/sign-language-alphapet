import sys, importlib.metadata

# Patch for Python < 3.11: packages_distributions() doesn't exist yet.
if sys.version_info < (3, 11) and not hasattr(importlib.metadata, "packages_distributions"):
    importlib.metadata.packages_distributions = lambda: {}

from fastapi import FastAPI
from app.routers.endpoint import router, load_keras_model

app = FastAPI(title="ASL Alphabet Classifier API")
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup():
    load_keras_model()
