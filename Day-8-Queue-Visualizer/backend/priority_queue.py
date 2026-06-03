# Priority Queue Implementation
# Real-life example: Hospital Emergency Patient System
# Concept: Patient with highest priority is served first

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def get_status(self, message, operation):
        return {
            "message": message,
            "operation": operation,
            "queue": self.queue,
            "size": len(self.queue),
            "is_empty": len(self.queue) == 0
        }

    def enqueue(self, patient_name, priority):
        patient = {
            "name": patient_name,
            "priority": priority
        }

        self.queue.append(patient)

        # Lower number means higher priority
        self.queue.sort(key=lambda patient: patient["priority"])

        return self.get_status(
            f"{patient_name} added with priority {priority}",
            "enqueue"
        )

    def dequeue(self):
        if len(self.queue) == 0:
            return self.get_status(
                "Priority Queue is empty. No patient to serve.",
                "dequeue"
            )

        served_patient = self.queue.pop(0)

        return self.get_status(
            f"{served_patient['name']} served first due to priority {served_patient['priority']}",
            "dequeue"
        )

    def peek(self):
        if len(self.queue) == 0:
            return self.get_status(
                "Priority Queue is empty.",
                "peek"
            )

        first_patient = self.queue[0]

        return self.get_status(
            f"{first_patient['name']} is next with priority {first_patient['priority']}",
            "peek"
        )

    def clear_queue(self):
        self.queue.clear()

        return self.get_status(
            "Priority Queue cleared successfully",
            "clear"
        )