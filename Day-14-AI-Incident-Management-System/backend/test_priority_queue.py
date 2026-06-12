from services.priority_queue import PriorityQueue

pq = PriorityQueue()

incident1 = {
    "id": 1,
    "description": "API timeout issue",
    "category": "Application Error",
    "severity": "Low"
}

incident2 = {
    "id": 2,
    "description": "Database crashed after deployment",
    "category": "Database Failure",
    "severity": "Critical"
}

incident3 = {
    "id": 3,
    "description": "Payment service exception",
    "category": "Application Error",
    "severity": "High"
}

incident4 = {
    "id": 4,
    "description": "Multiple failed login attempts",
    "category": "Security Incident",
    "severity": "Critical"
}

pq.enqueue(incident1)
pq.enqueue(incident2)
pq.enqueue(incident3)
pq.enqueue(incident4)

print("Priority Queue Order:")
for incident in pq.display():
    print(incident["id"], incident["description"], "-", incident["severity"])

print("\nHandling first incident:")
first_incident = pq.dequeue()
print(first_incident["description"], "-", first_incident["severity"])

print("\nQueue after dequeue:")
for incident in pq.display():
    print(incident["id"], incident["description"], "-", incident["severity"])