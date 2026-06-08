import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [symbol, setSymbol] = useState("AAPL");
  const [orderType, setOrderType] = useState("BUY");
  const [quantity, setQuantity] = useState("");
  const [queueInfo, setQueueInfo] = useState(null);
  const [latestOrder, setLatestOrder] = useState(null);
  const [executedOrders, setExecutedOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchQueue = async () => {
    const res = await axios.get(`${API}/queue-info`);
    setQueueInfo(res.data);
  };

  useEffect(() => {
    fetchQueue();
  }, []);

  const placeOrder = async () => {
    if (!symbol || !quantity) return;

    setLoading(true);
    try {
      const res = await axios.post(`${API}/order`, {
        symbol,
        order_type: orderType,
        quantity: Number(quantity),
      });

      setLatestOrder(res.data.order);
      setQuantity("");
      await fetchQueue();
    } catch (err) {
      alert("Failed to place order");
    }
    setLoading(false);
  };

  const processOrder = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API}/process-order`);

      if (res.data.executed_order) {
        setExecutedOrders((prev) => [
          {
            ...res.data.executed_order,
            executed_at: new Date().toLocaleTimeString(),
          },
          ...prev,
        ]);
      }

      await fetchQueue();
    } catch (err) {
      alert("Failed to process order");
    }
    setLoading(false);
  };

  const orders = queueInfo?.orders || [];
  const capacity = queueInfo?.queue_capacity || 10;

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>📈 Stock Order Processing System</h1>
          <p>DSA Circular Queue + ML Linear Regression Trading Engine</p>
        </div>
        <div className="status">
          <span></span> Backend Connected
        </div>
      </header>

      <main className="dashboard">
        <section className="panel left-panel">
          <h2>🛒 Place New Order</h2>
          <p className="subtext">Add a new trade order to the circular queue</p>

          <label>Stock Symbol</label>
          <input
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            placeholder="AAPL, TSLA, NVDA"
          />

          <label>Order Type</label>
          <div className="type-buttons">
            <button
              className={orderType === "BUY" ? "buy active" : "buy"}
              onClick={() => setOrderType("BUY")}
            >
              ↗ BUY
            </button>
            <button
              className={orderType === "SELL" ? "sell active" : "sell"}
              onClick={() => setOrderType("SELL")}
            >
              ↘ SELL
            </button>
          </div>

          <label>Quantity</label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            placeholder="Enter quantity"
          />

          <button className="primary-btn" onClick={placeOrder} disabled={loading}>
            🚀 Place Order
          </button>

          <div className="divider">OR</div>

          <button className="process-btn" onClick={processOrder} disabled={loading}>
            ⚡ Process Next Order
          </button>

          <p className="hint">Executes highest ML-priority order from queue</p>
        </section>

        <section className="panel center-panel">
          <div className="panel-head">
            <div>
              <h2>🔁 Circular Queue</h2>
              <p className="subtext">Order Buffer using Circular Queue</p>
            </div>
            <div className="counter">
              {orders.length} / {capacity}
              <span>Orders</span>
            </div>
          </div>

          <div className="queue-row">
            {Array.from({ length: capacity }).map((_, index) => {
              const order = orders[index];

              return (
                <div
                  key={index}
                  className={`queue-slot ${order ? "filled" : ""} ${
                    order?.order_type === "BUY" ? "buy-border" : ""
                  } ${order?.order_type === "SELL" ? "sell-border" : ""}`}
                >
                  <span className="index">{index}</span>

                  {order ? (
                    <>
                      <strong>{order.symbol}</strong>
                      <em className={order.order_type === "BUY" ? "green" : "red"}>
                        {order.order_type}
                      </em>
                      <small>Qty {order.quantity}</small>
                      <small>Score {order.priority_score}</small>
                    </>
                  ) : (
                    <span className="empty">Empty</span>
                  )}
                </div>
              );
            })}
          </div>

          <div className="queue-meta">
            <div>
              <strong>{capacity}</strong>
              <span>Capacity</span>
            </div>
            <div>
              <strong>{orders.length}</strong>
              <span>Current Orders</span>
            </div>
            <div>
              <strong>{queueInfo?.front_index ?? -1}</strong>
              <span>Front</span>
            </div>
            <div>
              <strong>{queueInfo?.rear_index ?? -1}</strong>
              <span>Rear</span>
            </div>
          </div>
        </section>

        <section className="panel right-panel">
          <h2>🧠 ML Prediction Analytics</h2>
          <p className="subtext">Linear Regression Model</p>

          {latestOrder ? (
            <>
              <div className="price-grid">
                <div>
                  <span>Current Price</span>
                  <strong>${latestOrder.current_price}</strong>
                </div>
                <div>
                  <span>Predicted Close</span>
                  <strong>${latestOrder.predicted_next_close}</strong>
                </div>
              </div>

              <div className="return-card">
                <span>Expected Return</span>
                <strong
                  className={
                    latestOrder.expected_return_percent >= 0 ? "green" : "red"
                  }
                >
                  {latestOrder.expected_return_percent}%
                </strong>
                <p>Priority Score: {latestOrder.priority_score}</p>
              </div>

              <div className="metrics">
                <h3>Model Performance</h3>
                <div>
                  <span>MAE</span>
                  <strong>{latestOrder.model_metrics?.mae}</strong>
                </div>
                <div>
                  <span>MSE</span>
                  <strong>{latestOrder.model_metrics?.mse}</strong>
                </div>
                <div>
                  <span>R²</span>
                  <strong>{latestOrder.model_metrics?.r2_score}</strong>
                </div>
              </div>

              <div className="features">
                <span>open</span>
                <span>high</span>
                <span>low</span>
                <span>volume</span>
                <span>previous_close</span>
              </div>
            </>
          ) : (
            <div className="placeholder">
              Place an order to view ML prediction analytics.
            </div>
          )}
        </section>
      </main>

      <section className="history panel">
        <div className="history-head">
          <div>
            <h2>⚙ Executed Orders History</h2>
            <p className="subtext">Recently processed orders</p>
          </div>
          <button onClick={() => setExecutedOrders([])}>Clear History</button>
        </div>

        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Symbol</th>
              <th>Type</th>
              <th>Qty</th>
              <th>Current</th>
              <th>Predicted</th>
              <th>Return</th>
              <th>Score</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {executedOrders.map((order, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{order.symbol}</td>
                <td className={order.order_type === "BUY" ? "green" : "red"}>
                  {order.order_type}
                </td>
                <td>{order.quantity}</td>
                <td>${order.current_price}</td>
                <td>${order.predicted_next_close}</td>
                <td>{order.expected_return_percent}%</td>
                <td>{order.priority_score}</td>
                <td>{order.executed_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

export default App;