import joblib
import numpy as np


model = joblib.load("model.pkl")


def predict_performance_score_ml(features):
    input_features = np.array([
        [
            features["total_lines"],
            features["loop_count"],
            features["if_count"],
            features["function_count"],
            features["recursion_count"],
            features["max_loop_depth"],
        ]
    ])

    predicted_score = model.predict(input_features)[0]

    return round(predicted_score, 2)


def get_ml_runtime_label(predicted_score):
    if predicted_score >= 80:
        return "Light Runtime"

    if predicted_score >= 50:
        return "Moderate Runtime"

    return "Heavy Runtime"
