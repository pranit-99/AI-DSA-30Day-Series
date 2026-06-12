from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from services.incident_manager import IncidentManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = IncidentManager()


class IncidentRequest(BaseModel):
    description: str


class ActionRequest(BaseModel):
    incident_id: int
    action: str


class UndoRequest(BaseModel):
    incident_id: int


@app.get("/")
def home():
    return {
        "message": "AI Incident Management System Backend Running"
    }


@app.post("/predict-incident")
def predict_incident(request: IncidentRequest):
    incident = manager.create_incident(request.description)

    return {
        "message": "Incident created successfully",
        "incident": incident,
        "incidents": manager.get_incidents()
    }


@app.get("/incidents")
def get_incidents():
    return {
        "incidents": manager.get_incidents()
    }


@app.post("/handle-next")
def handle_next_incident():
    incident = manager.handle_next_incident()

    if incident is None:
        return {
            "message": "No incidents available",
            "incident": None
        }

    return {
        "message": "Next highest priority incident selected",
        "incident": incident
    }


@app.post("/add-action")
def add_action(request: ActionRequest):
    result = manager.add_action_to_incident(
        request.incident_id,
        request.action
    )

    return result


@app.post("/undo-action")
def undo_action(request: UndoRequest):
    result = manager.undo_action_for_incident(request.incident_id)

    return result


@app.get("/actions/{incident_id}")
def get_actions(incident_id: int):
    actions = manager.get_actions_for_incident(incident_id)

    return {
        "incident_id": incident_id,
        "actions": actions
    }