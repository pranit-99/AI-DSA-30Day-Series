# Circular Queue Implementation
# Real-life example: CPU Round Robin Scheduling
# Concept: Fixed-size queue where rear can rotate back to index 0

class CircularQueue:
    def __init__(self, capacity = 5):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1
        self.size = 0

    def get_status(self, message, operation):
        return {
            "message": message,
            "operation": operation,
            "queue": self.queue,
            "front": self.front,
            "rear": self.rear,
            "size": self.size,
            "capacity": self.capacity,
            "is_empty": self.size == 0,
            "is_full": self.size == self.capacity
        }
    
    def enqueue(self, task_name):
        if self.size == self.capacity:
            return self.get_status("Circular Queue is full. No slot available.", "enqueue")
        
        if self.size == 0:
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity

        self.queue[self.rear] = task_name
        self.size += 1

        return self.get_status(f"{task_name} added to CPU task queue", "enqueue")
    
    def dequeue(self):
        if self.size == 0:
            return self.get_status("Circular Queue is empty. No task to process.", "dequeue")
        
        removed_task = self.queue[self.front]
        self.queue[self.front] = None
        self.size -= 1

        if self.size == 0:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
            
        return self.get_status(f"{removed_task} processed and removed from queue", "dequeue")
    
    def peek(self):
        if self.size == 0:
            return self.get_status("Circular Queue is empty.", "peek")

        return self.get_status(
            f"{self.queue[self.front]} is the next CPU task",
            "peek"
        )

    def clear_queue(self):
        self.queue = [None] * self.capacity
        self.front = -1
        self.rear = -1
        self.size = 0

        return self.get_status("Circular Queue cleared successfully", "clear")

        

