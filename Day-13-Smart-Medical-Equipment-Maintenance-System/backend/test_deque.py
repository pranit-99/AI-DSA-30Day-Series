from maintenance_logic import MedicalEquipmentDeque

maintenance_queue = MedicalEquipmentDeque(5)

print(maintenance_queue.add_rear("ECG Machine - Routine Check"))
print(maintenance_queue.add_rear("Patient Monitor - Routine Check"))
print(maintenance_queue.add_front("Ventilator - Critical Failure"))
print(maintenance_queue.add_front("MRI System - Critical Error"))

print("Current Queue:")
print(maintenance_queue.get_queue())

print("Processing Next Request:")
print(maintenance_queue.remove_front())

print("Queue After Processing:")
print(maintenance_queue.get_queue())