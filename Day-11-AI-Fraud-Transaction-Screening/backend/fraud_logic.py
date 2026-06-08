class CircularTransactionQueue:
    def __init__(self, size=5):
        self.size = size
        self.queue = [None] * size
        self.front = -1
        self.rear = -1

    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return (self.rear + 1) % self.size == self.front

    def enqueue(self, transaction):
        if self.is_full():
            # overwrite oldest transaction
            self.front = (self.front + 1) % self.size

        if self.is_empty():
            self.front = 0

        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = transaction

    def get_transactions(self):
        if self.is_empty():
            return []

        transactions = []
        i = self.front

        while True:
            transactions.append(self.queue[i])

            if i == self.rear:
                break

            i = (i + 1) % self.size

        return transactions

    def get_queue_status(self):
        return {
            "size": self.size,
            "front": self.front,
            "rear": self.rear,
            "is_empty": self.is_empty(),
            "is_full": self.is_full(),
            "transactions": self.get_transactions()
        }