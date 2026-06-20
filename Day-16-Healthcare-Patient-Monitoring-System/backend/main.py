from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from patient import Patient
from vital_reading import VitalReading
from monitoring_system import MonitoringSystem


app = FastAPI(title="Healthcare Patient Monitoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


patient = Patient(
    "P0001",
    78,
    "Male",
    "Pneumonia",
    "Emergency",
    2
)

system = MonitoringSystem(patient)


class VitalInput(BaseModel):
    timestamp: str
    heart_rate: float
    spo2: float
    respiratory_rate: float
    systolic_bp: float
    diastolic_bp: float
    temperature: float


class EventInput(BaseModel):
    event: str


@app.get("/")
def home():
    return {
        "message": "Healthcare Patient Monitoring API is running"
    }


@app.get("/patient")
def get_patient():
    return system.get_patient_info()


@app.post("/readings")
def add_reading(data: VitalInput):
    reading = VitalReading(
        data.timestamp,
        data.heart_rate,
        data.spo2,
        data.respiratory_rate,
        data.systolic_bp,
        data.diastolic_bp,
        data.temperature
    )

    return system.add_vital_reading(reading)


@app.get("/readings/latest")
def latest_reading():
    return system.get_latest_reading()


@app.get("/readings/history")
def reading_history():
    return system.get_reading_history()


@app.delete("/readings/undo")
def undo_reading():
    return system.undo_latest_reading()


@app.post("/events")
def add_event(data: EventInput):
    return system.add_medical_event(data.event)


@app.get("/events/history")
def event_history():
    return {
        "events": system.get_event_history()
    }


@app.get("/predict/heart-rate")
def predict_heart_rate():
    return system.predict_heart_rate_from_latest()