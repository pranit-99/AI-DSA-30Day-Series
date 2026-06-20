class VitalReading:
    def __init__(
        self,
        timestamp,
        heart_rate,
        spo2,
        respiratory_rate,
        systolic_bp,
        diastolic_bp,
        temperature
    ):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.spo2 = spo2
        self.respiratory_rate = respiratory_rate
        self.systolic_bp = systolic_bp
        self.diastolic_bp = diastolic_bp
        self.temperature = temperature

    def get_reading_info(self):
        return {
            "timestamp": self.timestamp,
            "heart_rate": self.heart_rate,
            "spo2": self.spo2,
            "respiratory_rate": self.respiratory_rate,
            "systolic_bp": self.systolic_bp,
            "diastolic_bp": self.diastolic_bp,
            "temperature": self.temperature
        }