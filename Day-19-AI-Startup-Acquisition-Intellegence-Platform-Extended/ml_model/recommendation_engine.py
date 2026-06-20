import joblib
import os
import pandas as pd


def get_recommendation(startup_input):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "models", "random_forest_model.pkl")
    FEATURES_PATH = os.path.join(BASE_DIR, "models", "features.pkl")

    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)

    input_df = pd.DataFrame([startup_input])
    input_df = input_df[features]

    prediction = model.predict(input_df)[0]
    acquisition_probability = model.predict_proba(input_df)[0][1]

    health_score = round(acquisition_probability * 100, 2)

    if prediction == 1:
        prediction_label = "Likely to be Acquired"
    else:
        prediction_label = "Likely to be Closed"

    if health_score >= 80:
        risk_level = "Low Risk"
    elif health_score >= 60:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"

    if health_score >= 80:
        recommendation = "Strong Acquisition Candidate"
    elif health_score >= 60:
        recommendation = "Investment / Monitor Candidate"
    elif health_score >= 40:
        recommendation = "High Risk, Needs More Validation"
    else:
        recommendation = "Reject / Avoid"

    return {
        "prediction": prediction_label,
        "acquisition_probability": health_score,
        "startup_health_score": health_score,
        "risk_level": risk_level,
        "recommendation": recommendation
    }


if __name__ == "__main__":
    df = pd.read_csv("data/startup_data.csv")
    features = joblib.load("models/features.pkl")

    startup_input = df[features].iloc[0].to_dict()

    result = get_recommendation(startup_input)

    print("\nRecommendation Result\n")
    print(result)