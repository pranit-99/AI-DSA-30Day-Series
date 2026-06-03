from fastapi import FastAPI
from pydantic import BaseModel
from bug_classifier import BugClassifier
from priority_queue import BugPriorityQueue
from evaluate_model import get_model_metrics
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Bug Ticket Priority Classifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = BugClassifier()
bug_queue = BugPriorityQueue()


class BugTicket(BaseModel):
    title: str
    description: str


@app.get("/")
def home():
    return {
        "message": "AI Bug Ticket Priority Classifier API is running"
    }


@app.post("/add-bug")
def add_bug(ticket: BugTicket):
    priority_number, priority_label = classifier.classify_bug(ticket.description)

    bug_queue.add_bug(
        priority_number,
        ticket.title,
        ticket.description
    )

    return {
        "message": "Bug added successfully",
        "title": ticket.title,
        "description": ticket.description,
        "priority_number": priority_number,
        "priority_label": priority_label,
        "current_queue": bug_queue.get_all_bugs()
    }


@app.get("/queue")
def get_queue():
    return {
        "queue": bug_queue.get_all_bugs()
    }


@app.get("/next-bug")
def get_next_bug():
    return {
        "next_bug": bug_queue.get_next_bug()
    }

@app.get("/model-metrics")
def model_metrics():
    return get_model_metrics()