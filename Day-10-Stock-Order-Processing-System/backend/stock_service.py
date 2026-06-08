import yfinance as yf


def get_stock_candles(symbol: str, period: str = "3mo", interval: str = "1d"):
    stock = yf.Ticker(symbol.upper())

    df = stock.history(period=period, interval=interval)

    if df.empty:
        return {
            "error": "No stock data found. Please check the stock symbol."
        }

    df = df.reset_index()

    return {
        "symbol": symbol.upper(),
        "candles": [
            {
                "date": str(row["Date"].date()),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
                "volume": int(row["Volume"])
            }
            for _, row in df.iterrows()
        ],
        "latest_price": round(df["Close"].iloc[-1], 2)
    }