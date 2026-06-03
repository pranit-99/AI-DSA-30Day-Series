import heapq

class BugPriorityQueue:
    def __init__(self):
        self.queue = []

        self.priority_lables = {
            1: "Critical",
            2: "High",
            3: "Medium",
            4: "Low"
        }

    def add_bug(self, priority, bug_title, bug_description):
        heapq.heappush(self.queue, (priority, bug_title, bug_description))

    def get_next_bug(self):
        if self.queue:
            priority, bug_title,bug_description = heapq.heappop(self.queue)

            return {
                "priority_number": priority,
                "priority_label": self.priority_lables[priority],
                "bug_title": bug_title,
                "bug_description":bug_description
            }
        return None
    
    def get_all_bugs(self):
        sorted_queue = sorted(self.queue)
        return [
            {
                "priority_number": priority,
                "priority_label": self.priority_lables[priority],
                "bug_title": bug_title,
                "bug_description": bug_description
            }
            for priority, bug_title, bug_description in sorted_queue
        ]