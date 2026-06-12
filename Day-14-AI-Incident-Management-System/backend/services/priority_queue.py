class PriorityQueue:
    def __init__(self):
        self.queue = []

    def get_priority_value(self, severity):
        if severity == "Critical":
            return 1
        elif severity == "High":
            return 2
        elif severity == "Medium":
            return 3
        elif severity == "Low":
            return 4
        else:
            return 5
        
    def enqueue(self, incident):
        priority = self.get_priority_value(incident["severity"])

        new_item = {
            "priority": priority,
            "incident": incident
        }

        if len(self.queue) == 0:
            self.queue.append(new_item)
            return
        
        inserted = False

        for index in range(len(self.queue)):
            if priority < self.queue[index] ["priority"]:
                self.queue.insert(index, new_item)
                inserted = True
                break

        if inserted == False:
            self.queue.append(new_item)

    def dequeue(self):
        if len(self.queue) == 0:
            return None
        
        first_item = self.queue[0]
        del self.queue[0]

        return first_item["incident"]
    
    def display(self):
        incidents = []

        for item in self.queue:
            incidents.append(item["incident"])

        return incidents
    