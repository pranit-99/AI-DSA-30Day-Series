import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

def train_failure_model():
    data = {
        "equipment_age": [1, 2, 3, 5, 7, 8, 10, 12, 4, 6],
        "usage_hours": [1000, 2500, 4000, 7000, 9000, 12000, 15000, 18000, 5000, 8500],
        "previous_breakdowns": [0, 0, 1, 2, 3, 4, 6, 7, 1, 3],
        "maintenance_frequency": [30, 45, 60, 75, 90, 100, 120, 150, 60, 90],
        "error_count": [2, 5, 8, 15, 25, 35, 50, 65, 10, 22],
        "failure_likely": [0, 0, 0, 0, 1, 1, 1, 1, 0, 1]
    }

    df = pd.DataFrame(data)

    x = df[
        [
            "equipment_age",
            "usage_hours",
            "previous_breakdowns",
            "maintenance_frequency",
            "error_count"
        ]
    ]

    y = df["failure_likely"]

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    model = LogisticRegression(max_iter=1000)
    model.fit(x_scaled, y)

    return model, scaler


failure_model, scaler = train_failure_model()


def predict_failure(equipment_age, usage_hours, previous_breakdowns, maintenance_frequency, error_count):
    input_data = pd.DataFrame(
        [[
            equipment_age,
            usage_hours,
            previous_breakdowns,
            maintenance_frequency,
            error_count
        ]],
        columns=[
            "equipment_age",
            "usage_hours",
            "previous_breakdowns",
            "maintenance_frequency",
            "error_count"
        ]
    )

    input_scaled = scaler.transform(input_data)

    prediction = failure_model.predict(input_scaled)[0]
    probability = failure_model.predict_proba(input_scaled)[0][1]

    return {
        "prediction": int(prediction),
        "failure_probability": float(round(probability * 100, 2))
    }

def get_risk_level(probability):

    if probability >= 80:
        return "High Risk"

    elif probability >= 50:
        return "Medium Risk"

    else:
        return "Low Risk"