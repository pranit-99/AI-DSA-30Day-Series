from services.stack_manager import StackManager

stack_manager = StackManager()

incident_id = 1

print("Adding Actions:")

print(stack_manager.push_action(incident_id, "Checked application logs"))
print(stack_manager.push_action(incident_id, "Restarted database service"))
print(stack_manager.push_action(incident_id, "Rolled back deployment"))

print("\nCurrent Stack:")
print(stack_manager.get_actions(incident_id))

print("\nUndo Latest Action:")
print(stack_manager.pop_action(incident_id))

print("\nStack After Undo:")
print(stack_manager.get_actions(incident_id))