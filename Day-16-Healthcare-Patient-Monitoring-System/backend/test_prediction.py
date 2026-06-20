from prediction_service import PredictionService

service = PredictionService()

sample_input = {
    "age": 78,
    "spo2": 94,
    "respiratory_rate": 20,
    "systolic_bp": 130,
    "diastolic_bp": 85,
    "temperature": 37.1,
    "overall_risk": 2,
    "comorbidity_count": 2
}

predicted_hr = service.predict_heart_rate(sample_input)

print("Predicted Heart Rate:", predicted_hr)