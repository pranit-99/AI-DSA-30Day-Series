from patient import Patient
from vital_reading import VitalReading
from stack_manager import Stack

patient = Patient(
    "P0001",
    78,
    "Male",
    "Pneumonia",
    "Emergency",
    2
)

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

vital_stack = Stack()

vital_stack.push(reading1)
vital_stack.push(reading2)

print("Patient Info:")
print(patient.get_patient_info())

print("\nLatest Vital Reading:")
latest = vital_stack.peek()
print(latest.get_reading_info())

print("\nUndo Latest Reading:")
removed = vital_stack.pop()
print(removed.get_reading_info())

print("\nCurrent Latest Reading:")
latest = vital_stack.peek()
print(latest.get_reading_info())