from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from stock_service import get_stock_candles
from ml_model import predict_next_close
from circular_queue import CircularQueue
from pydantic import BaseModel


class TradeOrder(BaseModel):
    symbol: str
    order_type: str
    quantity: int

order_queue = CircularQueue(10)


app = FastAPI(title="Stock Order Processing System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Stock Order Processing Backend Running"}


@app.get("/stock/{symbol}")
def stock_data(symbol: str):
    return get_stock_candles(symbol)

@app.get("/predict/{symbol}")
def predict_stock(symbol: str):
    stock_data = get_stock_candles(symbol)

    if "error" in stock_data:
        return stock_data

    prediction = predict_next_close(stock_data["candles"])

    return {
        "symbol": symbol.upper(),
        "prediction": prediction
    }

@app.post("/order")
def place_order(order: TradeOrder):

    stock_data = get_stock_candles(order.symbol)

    if "error" in stock_data:
        return stock_data

    prediction = predict_next_close(stock_data["candles"])

    if "error" in prediction:
        return prediction

    expected_return = prediction["expected_return_percent"]

    if order.order_type.upper() == "BUY":
        priority_score = expected_return
    elif order.order_type.upper() == "SELL":
        priority_score = -expected_return
    else:
        return {
            "error": "Invalid order type. Use BUY or SELL."
        }

    order_data = {
        "symbol": order.symbol.upper(),
        "order_type": order.order_type.upper(),
        "quantity": order.quantity,
        "current_price": prediction["current_price"],
        "predicted_next_close": prediction["predicted_next_close"],
        "expected_return_percent": expected_return,
        "priority_score": round(priority_score, 2),
        "model_metrics": prediction["model_metrics"]
    }

    success = order_queue.enqueue(order_data)

    if not success:
        return {
            "message": "Queue Full"
        }

    return {
        "message": "ML-Based Order Added to Circular Queue",
        "order": order_data
    }

@app.get("/queue")
def view_queue():

    return {
        "orders": order_queue.get_all_orders()
    }

@app.post("/process-order")
def process_order():

    order = order_queue.dequeue_highest_priority()

    if order is None:
        return {
            "message": "No Orders Available"
        }

    return {
        "message": "Highest ML-Priority Order Executed Successfully",
        "executed_order": order,
        "remaining_orders": order_queue.get_all_orders()
    }


@app.get("/queue-info")
def queue_info():

    orders = order_queue.get_all_orders()

    return {
        "queue_capacity": order_queue.size,
        "current_orders": len(orders),
        "front_index": order_queue.front,
        "rear_index": order_queue.rear,
        "is_empty": order_queue.is_empty(),
        "is_full": order_queue.is_full(),
        "orders": orders
    }