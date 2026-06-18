import joblib
import pandas as pd

class RiskPredictor:
    def __init__(self):
        self.model = joblib.load("../ml_model/portfolio_risk_model.pkl")

    def predict_risk(self, volatility, avg_return):
        input_data = pd.DataFrame([{
            "volatility": volatility,
            "avg_return": avg_return
        }])

        prediction = self.model.predict(input_data) [0]

        risk_mapping = {
            0: "Low Risk",
            1: "Medium Risk",
            2: "High Risk"
        }

        return risk_mapping[int(prediction)]
    
if __name__ == "__main__":
        predictor = RiskPredictor()

        result = predictor.predict_risk(
            volatility=0.065,
            avg_return=-0.005
        )

        print("Predicted Risk:", result)