from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from maintenance_logic import MedicalEquipmentDeque
from ml_model import predict_failure, get_risk_level


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

maintenance_queue = MedicalEquipmentDeque(10)


class EquipmentRequest(BaseModel):
    equipment_name: str
    equipment_type: str
    equipment_age: int
    usage_hours: int
    previous_breakdowns: int
    maintenance_frequency: int
    error_count: int


@app.get("/")
def home():
    return {
        "message": "Smart Medical Equipment Maintenance System API is running"
    }


@app.post("/predict-maintenance")
def predict_maintenance(request: EquipmentRequest):
    result = predict_failure(
        request.equipment_age,
        request.usage_hours,
        request.previous_breakdowns,
        request.maintenance_frequency,
        request.error_count
    )
    risk_level = get_risk_level(
    result["failure_probability"]
    )

    equipment_data = {
        "equipment_name": request.equipment_name,
        "equipment_type": request.equipment_type,
        "equipment_age": request.equipment_age,
        "usage_hours": request.usage_hours,
        "previous_breakdowns": request.previous_breakdowns,
        "maintenance_frequency": request.maintenance_frequency,
        "error_count": request.error_count,
        "prediction": result["prediction"],
        "failure_probability": result["failure_probability"]
    }

    if result["prediction"] == 1:
        queue_message = maintenance_queue.add_front(equipment_data)
        priority = "Critical"
    else:
        queue_message = maintenance_queue.add_rear(equipment_data)
        priority = "Routine"

    return {
        "prediction_result": result,
        "risk_level": risk_level,
        "priority": priority,
        "queue_message": queue_message,
        "current_queue": maintenance_queue.get_queue()
    }


@app.get("/queue")
def get_queue():
    return {
        "current_queue": maintenance_queue.get_queue()
    }


@app.delete("/process-next")
def process_next_request():
    processed_request = maintenance_queue.remove_front()

    if processed_request is None:
        return {
            "message": "No maintenance requests available"
        }

    return {
        "message": "Next maintenance request processed",
        "processed_request": processed_request,
        "remaining_queue": maintenance_queue.get_queue()
    }
