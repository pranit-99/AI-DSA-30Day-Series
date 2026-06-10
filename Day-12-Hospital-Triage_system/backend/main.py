from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os

from circular_queue import CircularQueue

app = FastAPI(title="Hospital Emergency Triage System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_PATH = os.path.join("model", "patient_triage_model.pkl")
model = joblib.load(MODEL_PATH)

patient_queue = CircularQueue(capacity=5)


class Patient(BaseModel):
    patient_id: str
    name: str
    age: int
    heart_rate: int
    blood_pressure: int
    oxygen_level: int
    temperature: float


def predict_triage(patient: Patient):
    features = [[
        patient.age,
        patient.heart_rate,
        patient.blood_pressure,
        patient.oxygen_level,
        patient.temperature
    ]]

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return {
        "prediction": "Critical" if prediction == 1 else "Normal",
        "critical_probability": round(float(probability), 2)
    }


@app.get("/")
def home():
    return {"message": "Hospital Emergency Triage API is running"}


@app.post("/add_patient")
def add_patient(patient: Patient):
    triage_result = predict_triage(patient)

    patient_data = {
        "patient_id": patient.patient_id,
        "name": patient.name,
        "age": patient.age,
        "heart_rate": patient.heart_rate,
        "blood_pressure": patient.blood_pressure,
        "oxygen_level": patient.oxygen_level,
        "temperature": patient.temperature,
        "prediction": triage_result["prediction"],
        "critical_probability": triage_result["critical_probability"]
    }

    queue_result = patient_queue.enqueue(patient_data)

    return {
        "message": queue_result["message"],
        "patient": patient_data,
        "queue_status": patient_queue.get_status()
    }


@app.post("/predict_patient")
def predict_patient(patient: Patient):
    triage_result = predict_triage(patient)

    return {
        "patient_id": patient.patient_id,
        "name": patient.name,
        "prediction": triage_result["prediction"],
        "critical_probability": triage_result["critical_probability"]
    }


@app.post("/attend_patient")
def attend_patient():
    result = patient_queue.dequeue()

    return {
        "message": result["message"],
        "attended_patient": result.get("patient"),
        "queue_status": patient_queue.get_status()
    }


@app.get("/next_patient")
def next_patient():
    patient = patient_queue.peek()

    return {
        "next_patient": patient,
        "queue_status": patient_queue.get_status()
    }

@app.get("/dashboard")
def dashboard():

    status = patient_queue.get_status()

    return {
        "total_patients_waiting": status["size"],
        "critical_patients": status["critical_patients"],
        "normal_patients": status["normal_patients"],
        "queue_full": status["is_full"],
        "next_patient": patient_queue.peek()
    }


@app.get("/queue_status")
def queue_status():
    return patient_queue.get_status()
