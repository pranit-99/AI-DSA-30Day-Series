import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    return data

def calculate_features(data):
    data["Daily_Return"] = data["Close"].pct_change()#calculates Current Price vs Previous Price
    average_return = data["Daily_Return"].mean()
    volatility = data["Daily_Return"].std()#Dtandard Deviation:- this mesaures Spread, Variation, Volatility in finance
    return average_return, volatility


if __name__ == "__main__":
    data = fetch_stock_data("AAPL")
    avg_return, volatility = calculate_features(data)

    print("Average Return:", avg_return)
    print("Volatility:", volatility)