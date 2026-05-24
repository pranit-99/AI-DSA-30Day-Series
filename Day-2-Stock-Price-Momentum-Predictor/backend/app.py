from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from stock_predictor import get_stock_prediction_summary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Stock Price Momentum Predictor API is running"}


@app.get("/predict/{symbol}")
def predict_stock(symbol: str):
    return get_stock_prediction_summary(symbol.upper())