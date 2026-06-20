import joblib
import pandas as pd


class PredictionService:
    def __init__(self):
        self.model = joblib.load("models/heart_rate_svr_model.pkl")
        self.scaler = joblib.load("models/heart_rate_scaler.pkl")

        self.features = [
            "age",
            "spo2",
            "respiratory_rate",
            "systolic_bp",
            "diastolic_bp",
            "temperature",
            "overall_risk",
            "comorbidity_count"
        ]

    def predict_heart_rate(self, input_data):
        input_df = pd.DataFrame([input_data], columns=self.features)

        input_scaled = self.scaler.transform(input_df)

        prediction = self.model.predict(input_scaled)

        return round(float(prediction[0]), 2)