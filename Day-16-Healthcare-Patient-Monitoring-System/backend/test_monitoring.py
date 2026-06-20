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

reading1 = VitalReading(
    "2025-01-02 14:00:00",
    82,
    96,
    18,
    120,
    80,
    36.7
)

reading2 = VitalReading(
    "2025-01-02 14:15:00",
    88,
    94,
    20,
    130,
    85,
    37.1
)

system.add_vital_reading(reading1)
system.add_vital_reading(reading2)

system.add_medical_event("Medication given: Paracetamol")
system.add_medical_event("Doctor reviewed patient condition")

print("Patient Info:")
print(system.get_patient_info())

print("\nLatest Reading:")
print(system.get_latest_reading())

print("\nReading History:")
print(system.get_reading_history())

print("\nEvent History:")
print(system.get_event_history())

print("\nUndo Latest Reading:")
print(system.undo_latest_reading())

print("\nReading History After Undo:")
print(system.get_reading_history())

print("\nEvent History After Undo:")
print(system.get_event_history())