import joblib
from services.priority_queue import PriorityQueue
from services.stack_manager import StackManager
from services.severity_manager import SeverityManager


class IncidentManager:
    def __init__(self):
        self.model = joblib.load("models/naive_bayes_model.pkl")
        self.vectorizer = joblib.load("models/vectorizer.pkl")
        self.priority_queue = PriorityQueue()
        self.stack_manager = StackManager()
        self.severity_manager = SeverityManager()
        self.incident_id = 1

    def create_incident(self, description):
        vector = self.vectorizer.transform([description])
        category = self.model.predict(vector)[0]
        severity = self.severity_manager.assign_severity(category, description)

        incident = {
            "id": self.incident_id,
            "description": description,
            "category": category,
            "severity": severity,
            "status": "Open"
        }

        self.stack_manager.create_stack_for_incident(self.incident_id)
        self.priority_queue.enqueue(incident)

        self.incident_id += 1

        return incident

    def get_incidents(self):
        return self.priority_queue.display()

    def handle_next_incident(self):
        return self.priority_queue.dequeue()

    def add_action_to_incident(self, incident_id, action):
        return self.stack_manager.push_action(incident_id, action)

    def undo_action_for_incident(self, incident_id):
        return self.stack_manager.pop_action(incident_id)

    def get_actions_for_incident(self, incident_id):
        return self.stack_manager.get_actions(incident_id)