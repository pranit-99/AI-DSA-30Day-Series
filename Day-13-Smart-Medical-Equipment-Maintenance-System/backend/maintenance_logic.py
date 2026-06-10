class MedicalEquipmentDeque:
    def __init__(self, size):
        self.size = size
        self.queue = [None] * size
        self.front = -1
        self.rear = -1

    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return (self.front == 0 and self.rear == self.size - 1) or (self.front == self.rear + 1)

    def add_front(self, equipment):
        if self.is_full():
            return "Maintenance queue is full"

        if self.is_empty():
            self.front = 0
            self.rear = 0

        elif self.front == 0:
            self.front = self.size - 1

        else:
            self.front = self.front - 1

        self.queue[self.front] = equipment
        return "Critical equipment added to front"

    def add_rear(self, equipment):
        if self.is_full():
            return "Maintenance queue is full"

        if self.is_empty():
            self.front = 0
            self.rear = 0

        elif self.rear == self.size - 1:
            self.rear = 0

        else:
            self.rear = self.rear + 1

        self.queue[self.rear] = equipment
        return "Routine equipment added to rear"

    def remove_front(self):
        if self.is_empty():
            return None

        removed_equipment = self.queue[self.front]
        self.queue[self.front] = None

        if self.front == self.rear:
            self.front = -1
            self.rear = -1

        elif self.front == self.size - 1:
            self.front = 0

        else:
            self.front = self.front + 1

        return removed_equipment

    def get_queue(self):
        result = []

        if self.is_empty():
            return result

        i = self.front

        while True:
            result.append(self.queue[i])

            if i == self.rear:
                break

            if i == self.size - 1:
                i = 0
            else:
                i = i + 1

        return result