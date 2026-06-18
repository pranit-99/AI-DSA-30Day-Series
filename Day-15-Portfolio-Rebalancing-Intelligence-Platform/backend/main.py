from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from finance_utils import fetch_stock_data, calculate_features
from model_utils import RiskPredictor
from stack import PortfolioStack
from priority_queue import RiskPriorityQueue


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = RiskPredictor()
portfolio_stack = PortfolioStack()
risk_queue = RiskPriorityQueue()


class PortfolioRequest(BaseModel):
    tickers: List[str]


class ChangeRequest(BaseModel):
    action: str
    reason: str


class RiskAssetRequest(BaseModel):
    ticker: str
    risk_score: int


@app.get("/")
def home():
    return {
        "message": "Portfolio Rebalancing Intelligence Platform Backend Running"
    }


@app.get("/predict-stock-risk/{ticker}")
def predict_stock_risk(ticker: str):
    data = fetch_stock_data(ticker)
    avg_return, volatility = calculate_features(data)

    risk = predictor.predict_risk(volatility, avg_return)

    return {
        "ticker": ticker.upper(),
        "average_return": round(avg_return, 6),
        "volatility": round(volatility, 6),
        "predicted_risk": risk
    }


@app.post("/analyze-portfolio")
def analyze_portfolio(portfolio: PortfolioRequest):
    results = []

    for ticker in portfolio.tickers:
        data = fetch_stock_data(ticker)
        avg_return, volatility = calculate_features(data)
        risk = predictor.predict_risk(volatility, avg_return)

        risk_score = 30 if risk == "Low Risk" else 60 if risk == "Medium Risk" else 90

        asset_result = {
            "ticker": ticker.upper(),
            "average_return": round(avg_return, 6),
            "volatility": round(volatility, 6),
            "predicted_risk": risk,
            "risk_score": risk_score
        }

        results.append(asset_result)
        risk_queue.insert(asset_result)

    return {
        "portfolio_analysis": results,
        "highest_risk_asset": risk_queue.peek(),
        "risk_ranking_heap": risk_queue.get_all_assets()
    }


@app.post("/rebalance-portfolio")
def rebalance_portfolio(portfolio: PortfolioRequest):
    recommendations = []

    for ticker in portfolio.tickers:
        data = fetch_stock_data(ticker)
        avg_return, volatility = calculate_features(data)
        risk = predictor.predict_risk(volatility, avg_return)

        if risk == "High Risk":
            action = f"Reduce {ticker.upper()} allocation"
            reason = "High volatility detected"
        elif risk == "Medium Risk":
            action = f"Monitor {ticker.upper()} allocation"
            reason = "Moderate volatility detected"
        else:
            action = f"Hold {ticker.upper()} allocation"
            reason = "Low volatility detected"

        recommendation = {
            "ticker": ticker.upper(),
            "risk": risk,
            "action": action,
            "reason": reason
        }

        recommendations.append(recommendation)
        portfolio_stack.push(recommendation)

    return {
        "message": "Rebalancing recommendations generated",
        "recommendations": recommendations,
        "stack_history": portfolio_stack.get_all_changes()
    }


@app.post("/add-change")
def add_change(change: ChangeRequest):
    change_data = change.model_dump()
    portfolio_stack.push(change_data)

    return {
        "message": "Portfolio change added successfully",
        "latest_change": change_data,
        "all_changes": portfolio_stack.get_all_changes()
    }


@app.delete("/undo-change")
def undo_change():
    removed_change = portfolio_stack.pop()

    return {
        "message": "Last portfolio change undone",
        "removed_change": removed_change,
        "remaining_changes": portfolio_stack.get_all_changes()
    }


@app.get("/changes")
def get_changes():
    return {
        "changes": portfolio_stack.get_all_changes(),
        "latest_change": portfolio_stack.peek()
    }


@app.post("/add-risk-asset")
def add_risk_asset(asset: RiskAssetRequest):
    asset_data = asset.model_dump()
    risk_queue.insert(asset_data)

    return {
        "message": "Asset added to risk priority queue",
        "asset": asset_data,
        "highest_risk_asset": risk_queue.peek(),
        "all_assets": risk_queue.get_all_assets()
    }


@app.get("/highest-risk-asset")
def highest_risk_asset():
    return {
        "highest_risk_asset": risk_queue.peek()
    }


@app.delete("/process-highest-risk-asset")
def process_highest_risk_asset():
    removed_asset = risk_queue.extract_max()

    return {
        "message": "Highest risk asset processed",
        "processed_asset": removed_asset,
        "remaining_assets": risk_queue.get_all_assets()
    }
