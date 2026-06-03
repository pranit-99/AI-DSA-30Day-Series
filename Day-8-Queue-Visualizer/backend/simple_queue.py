# Simple Queue Implementation
# Real-life example: Bank Token Counter System
# Concept: FIFO - First In, First Out

class SimpleQueue:
    def __init__(self):
        self.queue = []

    def get_status(self, message, operation):
        return {
            "message": message,
            "operation": operation,
            "queue": self.queue,
            "front": self.queue[0] if len(self.queue) > 0 else None,
            "rear": self.queue[-1] if len(self.queue) > 0 else None,
            "size": len(self.queue),
            "is_empty": len(self.queue) == 0
        }

    def enqueue(self, customer_name):
        self.queue.append(customer_name)
        return self.get_status(
            f"{customer_name} added to the queue",
            "enqueue"
        )

    def dequeue(self):
        if len(self.queue) == 0:
            return self.get_status(
                "Queue is empty. No customer to serve.",
                "dequeue"
            )

        served_customer = self.queue.pop(0)
        return self.get_status(
            f"{served_customer} has been served and removed from queue",
            "dequeue"
        )

    def peek(self):
        if len(self.queue) == 0:
            return self.get_status(
                "Queue is empty",
                "peek"
            )

        return self.get_status(
            f"{self.queue[0]} is next to be served",
            "peek"
        )

    def get_queue(self):
        return self.get_status(
            "Current queue status",
            "status"
        )

    def clear_queue(self):
        self.queue.clear()
        return self.get_status(
            "Queue cleared successfully",
            "clear"
        )