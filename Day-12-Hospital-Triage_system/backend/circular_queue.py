class CircularQueue:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def enqueue(self, patient):
        if self.is_full():
            return {
                "success": False,
                "message": "Queue is full. Cannot add more patients."
            }

        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity

        self.queue[self.rear] = patient
        self.size += 1

        return {
            "success": True,
            "message": "Patient added to queue successfully.",
            "patient": patient
        }

    def dequeue(self):
        if self.is_empty():
            return {
                "success": False,
                "message": "Queue is empty. No patient to attend."
            }

        patient = self.queue[self.front]
        self.queue[self.front] = None

        if self.size == 1:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity

        self.size -= 1

        return {
            "success": True,
            "message": "Patient attended successfully.",
            "patient": patient
        }

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[self.front]

    def get_status(self):
        patients = []
        critical_count = 0
        normal_count = 0

        if not self.is_empty():
            index = self.front
            count = 0

        for patient in patients:
            if patient["prediction"] == "Critical":
                critical_count += 1
            else:
                normal_count += 1

            while count < self.size:
                patients.append(self.queue[index])
                index = (index + 1) % self.capacity
                count += 1

        return {
            "capacity": self.capacity,
            "size": self.size,
            "front": self.front,
            "rear": self.rear,
            "is_empty": self.is_empty(),
            "is_full": self.is_full(),
            "critical_patients": critical_count,
            "normal_patients": normal_count,
            "patients": patients,
            "raw_queue": self.queue
        }