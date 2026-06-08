from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from model import Transaction
from fraud_logic import CircularTransactionQueue
from fraud_model import predict_transaction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transaction_queue = CircularTransactionQueue(size=5)


@app.get("/")
def home():
    return {
        "message": "AI Fraud Transaction Screening API is running"
    }


@app.post("/transaction")
def add_transaction(transaction: Transaction):
    transaction_data = transaction.dict()

    prediction_result = predict_transaction(transaction_data)

    enriched_transaction = {
        **transaction_data,
        **prediction_result
    }

    transaction_queue.enqueue(enriched_transaction)

    return {
        "message": "Transaction screened successfully",
        "transaction": enriched_transaction,
        "queue_status": transaction_queue.get_queue_status()
    }


@app.get("/transactions")
def get_transactions():
    return {
        "recent_transactions": transaction_queue.get_transactions(),
        "queue_status": transaction_queue.get_queue_status()
    }