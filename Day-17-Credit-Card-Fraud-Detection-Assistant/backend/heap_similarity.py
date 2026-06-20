import pandas as pd
import math


class MinHeap:
    def __init__(self):
        self.heap = []

    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return (2 * index) + 1

    def right_child(self, index):
        return (2 * index) + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, item):
        self.heap.append(item)
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, index):
        while index > 0:
            parent_index = self.parent(index)

            if self.heap[index][0] < self.heap[parent_index][0]:
                self.swap(index, parent_index)
                index = parent_index
            else:
                break

    def extract_min(self):
        if len(self.heap) == 0:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)

        return root

    def heapify_down(self, index):
        smallest = index

        left = self.left_child(index)
        right = self.right_child(index)

        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left

        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        if smallest != index:
            self.swap(index, smallest)
            self.heapify_down(smallest)


class TransactionSimilarity:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

        self.df = self.df[
            [
                "amt",
                "category",
                "state",
                "gender",
                "city_pop",
                "is_fraud"
            ]
        ].dropna()

    def calculate_similarity(self, input_transaction, past_transaction):
        score = 0

        amount_difference = abs(
            float(input_transaction["amt"]) - float(past_transaction["amt"])
        )

        population_difference = abs(
            float(input_transaction["city_pop"]) - float(past_transaction["city_pop"])
        )

        score += amount_difference / 1000
        score += population_difference / 100000

        if input_transaction["category"] != past_transaction["category"]:
            score += 1

        if input_transaction["state"] != past_transaction["state"]:
            score += 1

        if input_transaction["gender"] != past_transaction["gender"]:
            score += 0.5

        return score

    def find_similar_transactions(self, input_transaction, k=5):
        heap = MinHeap()

        for _, row in self.df.iterrows():
            past_transaction = {
                "amt": row["amt"],
                "category": row["category"],
                "state": row["state"],
                "gender": row["gender"],
                "city_pop": row["city_pop"],
                "is_fraud": row["is_fraud"]
            }

            similarity_score = self.calculate_similarity(
                input_transaction,
                past_transaction
            )

            heap.insert((similarity_score, past_transaction))

        similar_transactions = []

        for _ in range(k):
            nearest = heap.extract_min()

            if nearest is not None:
                score, transaction = nearest

                similar_transactions.append(
                    {
                        "similarity_score": round(score, 4),
                        "amount": transaction["amt"],
                        "category": transaction["category"],
                        "state": transaction["state"],
                        "gender": transaction["gender"],
                        "city_pop": transaction["city_pop"],
                        "result": "Fraud" if transaction["is_fraud"] == 1 else "Genuine"
                    }
                )

        return similar_transactions