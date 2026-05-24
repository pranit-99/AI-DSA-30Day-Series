import { useState } from "react";
import "./App.css";

function App() {
  const [symbol, setSymbol] = useState("");
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze() {
    if (!symbol.trim()) {
      setError("Please enter a stock symbol.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setStockData(null);

      const response = await fetch(
        `http://127.0.0.1:8000/predict/${symbol.toUpperCase()}`
      );

      if (!response.ok) throw new Error();

      const data = await response.json();
      setStockData(data);
    } catch {
      setError("Something went wrong. Please check the symbol or backend server.");
    } finally {
      setLoading(false);
    }
  }

  const volatility = stockData ? calculateVolatility(stockData.prices) : null;

  return (
    <div className="app">
      <div className="dashboard">
        <div className="header">
          <h1>Stock Price Momentum Predictor</h1>
          <p>Analyze stock momentum using Arrays, Sliding Window, and Regression.</p>
        </div>

        <div className="search-panel">
          <input
            type="text"
            placeholder="Enter stock symbol e.g. AAPL"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          />
          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Stock"}
          </button>
        </div>

        {error && <p className="error-message">{error}</p>}
        {loading && <p className="loading-message">Fetching stock analytics...</p>}

        {stockData && (
          <>
            <div className="top-visuals">
              <MomentumGauge momentum={stockData.momentum} />
              <VolatilityCard volatility={volatility} />
            </div>

            <div className="cards-grid">
              <Metric title="Stock Symbol" value={stockData.stock_symbol} />
              <Metric title="Actual Price" value={`$${stockData.actual_price}`} />
              <Metric title="Predicted Price" value={`$${stockData.predicted_price}`} />
              <Metric title="Model Error" value={stockData.mae} />
              <Metric title="Confidence" value={stockData.confidence} />
              <Metric title="Price Change" value={`${stockData.price_change_percent}%`} />
              <Metric title="Support Price" value={`$${stockData.support_price}`} />
              <Metric title="Resistance Price" value={`$${stockData.resistance_price}`} />
            </div>

            <div className="insight-box">
              <h3>AI Insight</h3>
              <p>{stockData.ai_insight}</p>
            </div>

            <div className="charts-layout">
              <div className="chart-section">
                <h3>Price History Line Chart</h3>
                <LineChart prices={stockData.prices} />
              </div>

              <div className="chart-section">
                <h3>Moving Average vs Price</h3>
                <DualLineChart
                  prices={stockData.prices}
                  movingAverages={stockData.moving_averages}
                />
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function Metric({ title, value }) {
  return (
    <div className="metric-card">
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}

function MomentumGauge({ momentum }) {
  const score = momentum === "Upward" ? 82 : momentum === "Stable" ? 50 : 25;

  return (
    <div className="visual-card">
      <h3>Momentum Gauge</h3>
      <div className="gauge">
        <div className="gauge-fill" style={{ width: `${score}%` }}></div>
      </div>
      <p className="gauge-label">{momentum}</p>
    </div>
  );
}

function VolatilityCard({ volatility }) {
  const level =
    volatility <= 1.5 ? "Low" : volatility <= 3.5 ? "Medium" : "High";

  return (
    <div className="visual-card">
      <h3>Volatility Score</h3>
      <p className="volatility-value">{volatility}%</p>
      <p className="volatility-level">{level} Volatility</p>
    </div>
  );
}

function LineChart({ prices }) {
  const points = createPoints(prices);

  return (
    <svg viewBox="0 0 700 240" className="line-chart">
      <polyline points={points.join(" ")} className="price-line" fill="none" />
      {points.map((point, index) => {
        const [x, y] = point.split(",");
        return <circle key={index} cx={x} cy={y} r="4" />;
      })}
    </svg>
  );
}

function DualLineChart({ prices, movingAverages }) {
  const trimmedPrices = prices.slice(prices.length - movingAverages.length);
  const combinedValues = [...trimmedPrices, ...movingAverages];

  const pricePoints = createPoints(trimmedPrices, combinedValues);
  const maPoints = createPoints(movingAverages, combinedValues);

  return (
    <>
      <svg viewBox="0 0 700 240" className="line-chart">
      <polyline
  points={pricePoints.join(" ")}
  className="price-polyline"
/>

<polyline
  points={maPoints.join(" ")}
  className="moving-average-polyline"
/>
      </svg>

      <div className="legend">
        <span><b className="blue-dot"></b>Price</span>
        <span><b className="orange-dot"></b>Moving Average</span>
      </div>
    </>
  );
}

function createPoints(values, scaleValues = values) {
  const width = 700;
  const height = 240;
  const padding = 30;

  const min = Math.min(...scaleValues);
  const max = Math.max(...scaleValues);

  return values.map((value, index) => {
    const x = padding + (index * (width - padding * 2)) / (values.length - 1);
    const y =
      height -
      padding -
      ((value - min) / (max - min || 1)) * (height - padding * 2);

    return `${x},${y}`;
  });
}

function calculateVolatility(prices) {
  const returns = [];

  for (let i = 1; i < prices.length; i++) {
    returns.push(((prices[i] - prices[i - 1]) / prices[i - 1]) * 100);
  }

  const avg = returns.reduce((sum, val) => sum + val, 0) / returns.length;
  const variance =
    returns.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / returns.length;

  return Math.sqrt(variance).toFixed(2);
}

export default App;