from stack_manager import Stack
from prediction_service import PredictionService


class MonitoringSystem:
    def __init__(self, patient):
        self.patient = patient
        self.vital_stack = Stack()
        self.event_stack = Stack()
        self.prediction_service = PredictionService()

    def add_vital_reading(self, reading):
        self.vital_stack.push(reading)
        self.event_stack.push(
            f"New vital reading added at {reading.timestamp}"
        )
        return reading.get_reading_info()

    def get_latest_reading(self):
        latest = self.vital_stack.peek()

        if latest is None:
            return {
                "message": "No vital readings available"
            }

        return latest.get_reading_info()

    def undo_latest_reading(self):
        removed = self.vital_stack.pop()

        if removed is None:
            return {
                "message": "No reading available to undo"
            }

        self.event_stack.push(
            f"Vital reading removed from {removed.timestamp}"
        )

        return {
            "message": "Latest reading removed successfully",
            "removed_reading": removed.get_reading_info()
        }

    def get_reading_history(self):
        readings = self.vital_stack.get_all()

        return [
            reading.get_reading_info()
            for reading in readings
        ]

    def add_medical_event(self, event):
        self.event_stack.push(event)

        return {
            "message": "Medical event added successfully",
            "event": event
        }

    def get_event_history(self):
        return self.event_stack.get_all()

    def get_patient_info(self):
        return self.patient.get_patient_info()
    
    def predict_heart_rate_from_latest(self):
        latest = self.vital_stack.peek()

        if latest is None:
            return {
                "message": "No latest reading available for prediction"
            }

        input_data = {
            "age": self.patient.age,
            "spo2": latest.spo2,
            "respiratory_rate": latest.respiratory_rate,
            "systolic_bp": latest.systolic_bp,
            "diastolic_bp": latest.diastolic_bp,
            "temperature": latest.temperature,
            "overall_risk": 2,
            "comorbidity_count": self.patient.comorbidity_count
        }

        predicted_hr = self.prediction_service.predict_heart_rate(input_data)

        self.event_stack.push(
            f"Heart rate predicted as {predicted_hr} BPM"
        )

        return {
            "predicted_heart_rate": predicted_hr,
            "unit": "BPM"
        }