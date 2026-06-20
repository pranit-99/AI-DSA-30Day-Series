from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fraud_detector import FraudDetector
from heap_similarity import TransactionSimilarity


app = FastAPI(title="Credit Card Fraud Detection Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fraud_detector = FraudDetector("../ml_model/model.pkl")
similarity_engine = TransactionSimilarity("data/transactions.csv")


class TransactionInput(BaseModel):
    amt: float
    category: str
    state: str
    gender: str
    city_pop: int = 50000


@app.get("/")
def home():
    return {
        "message": "Credit Card Fraud Detection Assistant API is running"
    }


@app.post("/predict")
def predict_fraud(transaction: TransactionInput):
    transaction_data = transaction.dict()

    prediction_result = fraud_detector.predict(transaction_data)

    similar_transactions = similarity_engine.find_similar_transactions(
        transaction_data,
        k=5
    )

    return {
        "input_transaction": transaction_data,
        "prediction": prediction_result["prediction"],
        "fraud_probability": prediction_result["fraud_probability"],
        "risk_level": prediction_result["risk_level"],
        "similar_transactions": similar_transactions
    }

@app.get("/stats")
def get_stats():
    df = similarity_engine.df

    total_transactions = len(df)
    fraud_transactions = int(df["is_fraud"].sum())
    genuine_transactions = total_transactions - fraud_transactions
    fraud_rate = (fraud_transactions / total_transactions) * 100

    return {
        "total_transactions": total_transactions,
        "fraud_transactions": fraud_transactions,
        "genuine_transactions": genuine_transactions,
        "fraud_rate": round(fraud_rate, 2)
    }


@app.get("/categories")
def get_categories():
    df = similarity_engine.df

    category_counts = df["category"].value_counts().head(20)

    return [
        {
            "category": category,
            "count": int(count)
        }
        for category, count in category_counts.items()
    ]


@app.get("/states")
def get_states():
    df = similarity_engine.df

    state_counts = df["state"].value_counts().head(10)

    return [
        {
            "state": state,
            "count": int(count)
        }
        for state, count in state_counts.items()
    ]


@app.get("/fraud-samples")
def get_fraud_samples():
    df = similarity_engine.df

    fraud_df = df[df["is_fraud"] == 1].head(10)

    return fraud_df.to_dict(orient="records")

@app.get("/fraud-example")
def fraud_example():
    fraud_row = similarity_engine.df[
        similarity_engine.df["is_fraud"] == 1
    ].iloc[0]

    return {
        "amt": fraud_row["amt"],
        "category": fraud_row["category"],
        "state": fraud_row["state"],
        "gender": fraud_row["gender"]
    }

@app.get("/model-fraud-example")
def model_fraud_example():
    fraud_df = similarity_engine.df[similarity_engine.df["is_fraud"] == 1]

    for _, row in fraud_df.iterrows():
        data = {
            "amt": float(row["amt"]),
            "category": row["category"],
            "state": row["state"],
            "gender": row["gender"],
            "city_pop": int(row["city_pop"])
        }

        result = fraud_detector.predict(data)

        if result["prediction"] == "Fraud":
            return {
                "amt": data["amt"],
                "category": data["category"],
                "state": data["state"],
                "gender": data["gender"],
                "city_pop": data["city_pop"],
                "prediction": result
            }

    return {"message": "No fraud-predicted sample found"}
