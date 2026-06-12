from services.incident_manager import IncidentManager

manager = IncidentManager()

manager.create_incident("API returning 500 error after deployment")
manager.create_incident("Database crashed after deployment")
manager.create_incident("Multiple failed login attempts detected")
manager.create_incident("VPN connection dropped suddenly")

print("Current Priority Queue:")
for incident in manager.get_incidents():
    print(
        incident["id"],
        incident["description"],
        "|",
        incident["category"],
        "|",
        incident["severity"]
    )

print("\nHandling Next Incident:")
next_incident = manager.handle_next_incident()
print(
    next_incident["id"],
    next_incident["description"],
    "|",
    next_incident["category"],
    "|",
    next_incident["severity"]
)

print("\nQueue After Handling One Incident:")
for incident in manager.get_incidents():
    print(
        incident["id"],
        incident["description"],
        "|",
        incident["category"],
        "|",
        incident["severity"]
    )