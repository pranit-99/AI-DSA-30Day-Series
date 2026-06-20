from patient import Patient
from vital_reading import VitalReading
from monitoring_system import MonitoringSystem

patient = Patient(
    "P0001",
    78,
    "Male",
    "Pneumonia",
    "Emergency",
    2
)

system = MonitoringSystem(patient)

reading = VitalReading(
    "2025-01-02 14:15:00",
    88,
    94,
    20,
    130,
    85,
    37.1
)

system.add_vital_reading(reading)

print("Latest Reading:")
print(system.get_latest_reading())

print("\nPredicted Heart Rate:")
print(system.predict_heart_rate_from_latest())

print("\nEvent History:")
print(system.get_event_history())