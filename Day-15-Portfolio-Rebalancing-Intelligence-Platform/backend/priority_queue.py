class RiskPriorityQueue:
    def __init__(self):
        self.heap = []

    def insert(self, asset):
        self.heap.append(asset)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self):
        if self.is_empty():
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        max_asset = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return max_asset

    def peek(self):
        if self.is_empty():
            return None
        return self.heap[0]

    def is_empty(self):
        return len(self.heap) == 0

    def get_all_assets(self):
        return self.heap

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2

        if index > 0 and self.heap[index]["risk_score"] > self.heap[parent_index]["risk_score"]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        largest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if left_child < len(self.heap) and self.heap[left_child]["risk_score"] > self.heap[largest]["risk_score"]:
            largest = left_child

        if right_child < len(self.heap) and self.heap[right_child]["risk_score"] > self.heap[largest]["risk_score"]:
            largest = right_child

        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._heapify_down(largest)


if __name__ == "__main__":
    queue = RiskPriorityQueue()

    queue.insert({"ticker": "AAPL", "risk_score": 35})
    queue.insert({"ticker": "TSLA", "risk_score": 92})
    queue.insert({"ticker": "NVDA", "risk_score": 80})
    queue.insert({"ticker": "JPM", "risk_score": 20})

    print("Heap:", queue.get_all_assets())
    print("Highest Risk:", queue.peek())
    print("Extract Max:", queue.extract_max())
    print("After Extract:", queue.get_all_assets())