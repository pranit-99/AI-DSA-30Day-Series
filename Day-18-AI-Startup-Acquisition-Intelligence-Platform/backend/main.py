from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="AI Startup Acquisition Intelligence Platform")


model = joblib.load("models/model.pkl")
feature_names = joblib.load("models/features.pkl")


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
        "message": "AI Startup Acquisition Intelligence Platform API"
    }


@app.post("/predict")
def predict_acquisition(data: StartupInput):
    input_data = pd.DataFrame([data.dict()])

    input_data = input_data[feature_names]

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0]

    if prediction == 1:
        result = "Likely to be Acquired"
        confidence = probability[1]
    else:
        result = "Likely to be Closed"
        confidence = probability[0]

    return {
        "prediction": result,
        "confidence": round(confidence * 100, 2)
    }

@app.post("/decision-path")
def decision_path(data: StartupInput):
    input_data = pd.DataFrame([data.dict()])
    input_data = input_data[feature_names]

    node_indicator = model.decision_path(input_data)
    leaf_id = model.apply(input_data)

    tree = model.tree_

    path = []

    sample_id = 0
    node_index = node_indicator.indices[
        node_indicator.indptr[sample_id]:node_indicator.indptr[sample_id + 1]
    ]

    for node_id in node_index:
        if leaf_id[sample_id] == node_id:
            continue

        feature_index = tree.feature[node_id]
        threshold = tree.threshold[node_id]
        feature_name = feature_names[feature_index]
        feature_value = input_data.iloc[0, feature_index]

        if feature_value <= threshold:
            direction = "Left"
            condition = f"{feature_name} <= {round(threshold, 2)}"
        else:
            direction = "Right"
            condition = f"{feature_name} > {round(threshold, 2)}"

        path.append({
            "feature": feature_name,
            "value": float(feature_value),
            "threshold": round(float(threshold), 2),
            "direction": direction,
            "condition": condition
        })

    prediction = model.predict(input_data)[0]

    final_prediction = (
        "Likely to be Acquired" if prediction == 1 else "Likely to be Closed"
    )

    return {
        "prediction": final_prediction,
        "decision_path": path
    }