# Double Ended Queue Implementation
# Real-life example: Browser History / Undo-Redo System
# Concept: Insertion and deletion can happen from both front and rear

class DequeQueue:
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

    def add_front(self, page_name):
        self.queue.insert(0, page_name)

        return self.get_status(
            f"{page_name} added at the front",
            "add_front"
        )

    def add_rear(self, page_name):
        self.queue.append(page_name)

        return self.get_status(
            f"{page_name} added at the rear",
            "add_rear"
        )

    def remove_front(self):
        if len(self.queue) == 0:
            return self.get_status(
                "Deque is empty. Nothing to remove from front.",
                "remove_front"
            )

        removed_page = self.queue.pop(0)

        return self.get_status(
            f"{removed_page} removed from the front",
            "remove_front"
        )

    def remove_rear(self):
        if len(self.queue) == 0:
            return self.get_status(
                "Deque is empty. Nothing to remove from rear.",
                "remove_rear"
            )

        removed_page = self.queue.pop()

        return self.get_status(
            f"{removed_page} removed from the rear",
            "remove_rear"
        )

    def peek_front(self):
        if len(self.queue) == 0:
            return self.get_status(
                "Deque is empty. No front page.",
                "peek_front"
            )

        return self.get_status(
            f"{self.queue[0]} is at the front",
            "peek_front"
        )

    def peek_rear(self):
        if len(self.queue) == 0:
            return self.get_status(
                "Deque is empty. No rear page.",
                "peek_rear"
            )

        return self.get_status(
            f"{self.queue[-1]} is at the rear",
            "peek_rear"
        )

    def clear_queue(self):
        self.queue.clear()

        return self.get_status(
            "Deque cleared successfully",
            "clear"
        )