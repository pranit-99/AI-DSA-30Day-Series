from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Allow backend to import files from ml_model folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
ML_MODEL_DIR = os.path.join(PROJECT_DIR, "ml_model")

sys.path.append(PROJECT_DIR)

from ml_model.recommendation_engine import get_recommendation
from ml_model.feature_importance import get_feature_importance
from ml_model.model_comparison import get_model_comparison


app = FastAPI(title="AI Startup Acquisition Intelligence Platform Extended")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StartupInput(BaseModel):
    age_first_funding_year: float
    age_last_funding_year: float
    relationships: int
    funding_rounds: int
    funding_total_usd: float
    milestones: int
    has_VC: int
    has_angel: int
    has_roundA: int
    has_roundB: int
    has_roundC: int
    has_roundD: int
    avg_participants: float
    is_top500: int


@app.get("/")
def home():
    return {
        "message": "AI Startup Acquisition Intelligence Platform Extended API"
    }


@app.post("/predict")
def predict_startup(data: StartupInput):
    startup_input = data.dict()

    result = get_recommendation(startup_input)

    return result


@app.get("/dashboard-metadata")
def dashboard_metadata():
    feature_importance = get_feature_importance()
    model_comparison = get_model_comparison()

    return {
        "feature_importance": feature_importance,
        "model_comparison": model_comparison
    }