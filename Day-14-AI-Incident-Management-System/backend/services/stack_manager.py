class StackManager:
    def __init__(self):
        self.stacks = {}

    def create_stack_for_incident(self, incident_id):
        if incident_id not in self.stacks:
            self.stacks[incident_id] = []

    def push_action(self, incident_id, action):
        self.create_stack_for_incident(incident_id)
        self.stacks[incident_id].append(action)

        return {
            "message": "Action added successfully",
            "incident_id": incident_id,
            "action": action,
            "current_stack": self.stacks[incident_id]
        }

    def pop_action(self, incident_id):
        self.create_stack_for_incident(incident_id)

        if len(self.stacks[incident_id]) == 0:
            return {
                "message": "No action to undo",
                "incident_id": incident_id,
                "undone_action": None,
                "current_stack": []
            }

        undone_action = self.stacks[incident_id][-1]
        del self.stacks[incident_id][-1]

        return {
            "message": "Latest action undone",
            "incident_id": incident_id,
            "undone_action": undone_action,
            "current_stack": self.stacks[incident_id]
        }

    def get_actions(self, incident_id):
        self.create_stack_for_incident(incident_id)
        return self.stacks[incident_id]