from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from simple_queue import SimpleQueue
from circular_queue import CircularQueue
from priority_queue import PriorityQueue
from deque_queue import DequeQueue

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# One queue object for our bank counter example
bank_queue = SimpleQueue()
cpu_queue = CircularQueue(capacity=5)
hospital_queue = PriorityQueue()
browser_history_queue = DequeQueue()


class CustomerRequest(BaseModel):
    customer_name: str

class TaskRequest(BaseModel):
    task_name: str

class PatientRequest(BaseModel):
    patient_name: str
    priority: int

class PageRequest(BaseModel):
    page_name: str

@app.get("/")
def home():
    return {"message": "Queue Visualizer Backend Running"}


@app.post("/simple-queue/enqueue")
def enqueue_customer(request: CustomerRequest):
    return bank_queue.enqueue(request.customer_name)


@app.delete("/simple-queue/dequeue")
def dequeue_customer():
    return bank_queue.dequeue()


@app.get("/simple-queue/peek")
def peek_customer():
    return bank_queue.peek()


@app.get("/simple-queue")
def get_simple_queue():
    return bank_queue.get_queue()

@app.delete("/simple-queue/clear")
def clear_simple_queue():
    return bank_queue.clear_queue()

#------------Circular Endpoints
@app.post("/circular-queue/enqueue")
def enqueue_task(request: TaskRequest):
    return cpu_queue.enqueue(request.task_name)


@app.delete("/circular-queue/dequeue")
def dequeue_task():
    return cpu_queue.dequeue()


@app.get("/circular-queue/peek")
def peek_task():
    return cpu_queue.peek()


@app.get("/circular-queue")
def get_circular_queue():
    return cpu_queue.get_status("Current circular queue status", "status")


@app.delete("/circular-queue/clear")
def clear_circular_queue():
    return cpu_queue.clear_queue()

#----------Priority Queue
@app.post("/priority-queue/enqueue")
def enqueue_patient(request: PatientRequest):
    return hospital_queue.enqueue(request.patient_name, request.priority)


@app.delete("/priority-queue/dequeue")
def dequeue_patient():
    return hospital_queue.dequeue()


@app.get("/priority-queue/peek")
def peek_patient():
    return hospital_queue.peek()


@app.get("/priority-queue")
def get_priority_queue():
    return hospital_queue.get_status("Current priority queue status", "status")


@app.delete("/priority-queue/clear")
def clear_priority_queue():
    return hospital_queue.clear_queue()

#---------------Dequeue------------------#

@app.post("/deque/add-front")
def add_page_front(request: PageRequest):
    return browser_history_queue.add_front(request.page_name)


@app.post("/deque/add-rear")
def add_page_rear(request: PageRequest):
    return browser_history_queue.add_rear(request.page_name)


@app.delete("/deque/remove-front")
def remove_page_front():
    return browser_history_queue.remove_front()


@app.delete("/deque/remove-rear")
def remove_page_rear():
    return browser_history_queue.remove_rear()


@app.get("/deque/peek-front")
def peek_page_front():
    return browser_history_queue.peek_front()


@app.get("/deque/peek-rear")
def peek_page_rear():
    return browser_history_queue.peek_rear()


@app.get("/deque")
def get_deque_queue():
    return browser_history_queue.get_status("Current deque status", "status")


@app.delete("/deque/clear")
def clear_deque_queue():
    return browser_history_queue.clear_queue()