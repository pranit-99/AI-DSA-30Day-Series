from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import CodeInput
from code_analyzer import analyze_code_structure
from ml_predictor import predict_performance_score_ml, get_ml_runtime_label

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Code Complexity Analyzer Backend Running"
    }


@app.post("/analyze")
def analyze_code(input_data: CodeInput):
    analysis_result = analyze_code_structure(input_data.code)

    if "error" in analysis_result:
        return {
            "message": "Code analysis failed",
            "analysis": analysis_result
        }

    ml_score = predict_performance_score_ml(analysis_result)
    ml_runtime_label = get_ml_runtime_label(ml_score)

    return {
        "message": "Code analyzed successfully",
        "analysis": analysis_result,
        "ml_prediction": {
    "predicted_performance_score": ml_score,
    "predicted_runtime_heaviness": ml_runtime_label
}
    }