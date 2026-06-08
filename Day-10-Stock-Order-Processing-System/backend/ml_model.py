import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def predict_next_close(candles):
    df = pd.DataFrame(candles)

    if len(df) < 10:
        return {
            "error": "Not enough data to train the model"
        }

    df["previous_close"] = df["close"].shift(1)
    df["next_close"] = df["close"].shift(-1)

    df = df.dropna()

    features = ["open", "high", "low", "volume", "previous_close"]

    X = df[features]
    y = df["next_close"]

    model = LinearRegression()
    model.fit(X, y)

    latest_row = df.iloc[-1][features].values.reshape(1, -1)
    predicted_price = model.predict(latest_row)[0]

    y_pred = model.predict(X)

    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    current_price = candles[-1]["close"]
    expected_return = ((predicted_price - current_price) / current_price) * 100

    return {
        "current_price": round(current_price, 2),
        "predicted_next_close": round(predicted_price, 2),
        "expected_return_percent": round(expected_return, 2),
        "model_metrics": {
            "mae": round(mae, 2),
            "mse": round(mse, 2),
            "r2_score": round(r2, 4)
        },
        "features_used": features
    }