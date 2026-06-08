class CircularQueue:

    def __init__(self, size=10):
        self.size = size
        self.queue = [None] * size

        self.front = -1
        self.rear = -1

    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return (self.rear + 1) % self.size == self.front

    def enqueue(self, item):

        if self.is_full():
            return False

        if self.is_empty():
            self.front = 0
            self.rear = 0

        else:
            self.rear = (self.rear + 1) % self.size

        self.queue[self.rear] = item

        return True

    def dequeue(self):

        if self.is_empty():
            return None

        item = self.queue[self.front]

        if self.front == self.rear:
            self.front = -1
            self.rear = -1

        else:
            self.front = (self.front + 1) % self.size

        return item

    def get_all_orders(self):

        if self.is_empty():
            return []

        orders = []

        i = self.front

        while True:

            orders.append(self.queue[i])

            if i == self.rear:
                break

            i = (i + 1) % self.size

        return orders
    
    def dequeue_highest_priority(self):
        if self.is_empty():
            return None

        orders = self.get_all_orders()

        highest_priority_order = max(
            orders,
            key=lambda order: order.get("priority_score", 0)
        )

        new_orders = [
            order for order in orders
            if order != highest_priority_order
        ]

        self.queue = [None] * self.size
        self.front = -1
        self.rear = -1

        for order in new_orders:
            self.enqueue(order)

        return highest_priority_order