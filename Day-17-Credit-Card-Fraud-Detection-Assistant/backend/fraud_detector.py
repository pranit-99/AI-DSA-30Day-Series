import pickle
import pandas as pd


class FraudDetector:
    def __init__(self, model_path="../ml_model/model.pkl"):
        with open(model_path, "rb") as file:
            self.model = pickle.load(file)

    def predict(self, transaction_data):
        input_df = pd.DataFrame([transaction_data])

        prediction = self.model.predict(input_df)[0]
        probability = self.model.predict_proba(input_df)[0]

        fraud_probability = probability[1] * 100

        return {
            "prediction": "Fraud" if prediction == 1 else "Genuine",
            "fraud_probability": round(fraud_probability, 2),
            "risk_level": self.get_risk_level(fraud_probability)
        }

    def get_risk_level(self, fraud_probability):
        if fraud_probability >= 70:
            return "High Risk"
        elif fraud_probability >= 40:
            return "Medium Risk"
        else:
            return "Low Risk"