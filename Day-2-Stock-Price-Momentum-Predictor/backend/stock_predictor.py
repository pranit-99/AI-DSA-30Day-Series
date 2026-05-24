"""from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


prices = [100, 102, 101, 105, 108, 110, 112]
window_size = 3


def create_training_data(prices, window_size):
    X = []
    y = []

    for i in range(len(prices) - window_size):
        window = prices[i:i + window_size]
        target = prices[i + window_size]

        X.append(window)
        y.append(target)

    return X, y


def calculate_moving_averages(prices, window_size):
    moving_averages = []

    for i in range(len(prices) - window_size):
        window = prices[i:i + window_size]
        moving_average = sum(window) / window_size
        moving_averages.append(moving_average)

    return moving_averages


def detect_momentum(moving_averages):
    latest_ma = moving_averages[-1]
    previous_ma = moving_averages[-2]

    if latest_ma > previous_ma:
        return "Upward"
    elif latest_ma < previous_ma:
        return "Downward"
    else:
        return "Stable"


def train_and_predict(X, y):
    X_train = X[:3]
    y_train = y[:3]

    X_test = X[3:]
    y_test = y[3:]

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    return y_test, predictions, mae


def get_stock_prediction_summary():
    X, y = create_training_data(prices, window_size)
    moving_averages = calculate_moving_averages(prices, window_size)
    momentum = detect_momentum(moving_averages)
    actual_values, predicted_values, mae = train_and_predict(X, y)

    latest_prediction = round(float(predicted_values[-1]), 2)
    latest_actual = actual_values[-1]

    result = {
        "stock_name": "Demo Stock",
        "prices": prices,
        "moving_averages": [round(ma, 2) for ma in moving_averages],
        "momentum": momentum,
        "actual_price": latest_actual,
        "predicted_price": latest_prediction,
        "mae": round(mae, 2)
    }

    return result


summary = get_stock_prediction_summary()

print(summary)"""
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


window_size = 3


def fetch_stock_prices(symbol):
    stock_data = yf.download(symbol, period="1mo", interval="1d")

    closing_prices = stock_data["Close"].squeeze().dropna().tolist()

    return [round(float(price), 2) for price in closing_prices]


def create_training_data(prices, window_size):
    X = []
    y = []

    for i in range(len(prices) - window_size):
        window = prices[i:i + window_size]
        target = prices[i + window_size]

        X.append(window)
        y.append(target)

    return X, y


def calculate_moving_averages(prices, window_size):
    moving_averages = []

    for i in range(len(prices) - window_size):
        window = prices[i:i + window_size]
        moving_average = sum(window) / window_size
        moving_averages.append(moving_average)

    return moving_averages


def detect_momentum(moving_averages):
    latest_ma = moving_averages[-1]
    previous_ma = moving_averages[-2]

    if latest_ma > previous_ma:
        return "Upward"
    elif latest_ma < previous_ma:
        return "Downward"
    else:
        return "Stable"


def train_and_predict(X, y):
    split_index = int(len(X) * 0.8)

    X_train = X[:split_index]
    y_train = y[:split_index]

    X_test = X[split_index:]
    y_test = y[split_index:]

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    return y_test, predictions, mae


def get_stock_prediction_summary(symbol="AAPL"):
    prices = fetch_stock_prices(symbol)

    X, y = create_training_data(prices, window_size)
    moving_averages = calculate_moving_averages(prices, window_size)
    momentum = detect_momentum(moving_averages)
    actual_values, predicted_values, mae = train_and_predict(X, y)

    latest_price = prices[-1]
    previous_price = prices[-2]

    price_change_percent = ((latest_price - previous_price) / previous_price) * 100

    support_price = min(prices)
    resistance_price = max(prices)

    if mae <= 2:
        confidence = "High"
    elif mae <= 5:
        confidence = "Medium"
    else:
        confidence = "Low"

    ai_insight = (
        f"{symbol.upper()} shows {momentum.lower()} momentum because the latest "
        f"moving average is {round(moving_averages[-1], 2)} compared to the previous "
        f"moving average of {round(moving_averages[-2], 2)}. "
        f"The model predicts the next price around {round(float(predicted_values[-1]), 2)} "
        f"with {confidence.lower()} confidence."
    )


    result = {
        "stock_symbol": symbol,
        "prices": prices,
        "moving_averages": [round(ma, 2) for ma in moving_averages],
        "momentum": momentum,
        "actual_price": actual_values[-1],
        "predicted_price": round(float(predicted_values[-1]), 2),
        "mae": round(mae, 2),
        "confidence": confidence,
        "support_price": support_price,
        "resistance_price": resistance_price,
        "price_change_percent": round(price_change_percent, 2),
        "ai_insight": ai_insight
    }

    return result