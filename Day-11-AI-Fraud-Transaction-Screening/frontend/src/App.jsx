import { useState } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    transaction_id: "",
    amount: "",
    transaction_count_last_hour: "",
    account_age_days: "",
    location_mismatch: "0",
  });

  const [transactions, setTransactions] = useState([]);
  const [queueStatus, setQueueStatus] = useState(null);
  const [latestAlert, setLatestAlert] = useState(null);

  const API_URL = "http://127.0.0.1:8000";

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const submitTransaction = async (e) => {
    e.preventDefault();

    const payload = {
      transaction_id: formData.transaction_id,
      amount: Number(formData.amount),
      transaction_count_last_hour: Number(formData.transaction_count_last_hour),
      account_age_days: Number(formData.account_age_days),
      location_mismatch: Number(formData.location_mismatch),
    };

    const response = await fetch(`${API_URL}/transaction`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    setTransactions(data.queue_status.transactions);
    setQueueStatus(data.queue_status);
    setLatestAlert(data.transaction);
  };

  return (
    <div className="app">
      <header>
        <h1>AI Fraud Transaction Screening</h1>
        <p>Circular Queue + Logistic Regression</p>
      </header>

      <main className="dashboard">
        <section className="panel form-panel">
          <h2>Transaction Feed</h2>

          <form onSubmit={submitTransaction}>
            <input
              name="transaction_id"
              placeholder="Transaction ID"
              value={formData.transaction_id}
              onChange={handleChange}
              required
            />

            <input
              name="amount"
              type="number"
              placeholder="Amount"
              value={formData.amount}
              onChange={handleChange}
              required
            />

            <input
              name="transaction_count_last_hour"
              type="number"
              placeholder="Transactions Last Hour"
              value={formData.transaction_count_last_hour}
              onChange={handleChange}
              required
            />

            <input
              name="account_age_days"
              type="number"
              placeholder="Account Age Days"
              value={formData.account_age_days}
              onChange={handleChange}
              required
            />

            <select
              name="location_mismatch"
              value={formData.location_mismatch}
              onChange={handleChange}
            >
              <option value="0">Normal Location</option>
              <option value="1">Location Mismatch</option>
            </select>

            <button type="submit">Screen Transaction</button>
          </form>
        </section>

        <section className="panel queue-panel">
          <h2>Recent Transaction Queue</h2>

          <div className="queue-list">
            {transactions.length === 0 ? (
              <p className="empty">No transactions screened yet.</p>
            ) : (
              transactions.map((txn, index) => (
                <div
                  key={txn.transaction_id}
                  className={`txn-card ${
                    txn.prediction === "Fraud" ? "fraud" : "legitimate"
                  }`}
                >
                  <div className="txn-top">
                    <strong>{txn.transaction_id}</strong>
                    <span>{txn.prediction}</span>
                  </div>

                  <p>Amount: ${txn.amount}</p>
                  <p>Fraud Probability: {txn.fraud_probability}</p>
                  <p>Queue Index: {index}</p>
                </div>
              ))
            )}
          </div>
        </section>

        <section className="panel alert-panel">
          <h2>Fraud Alert</h2>

          {latestAlert ? (
            <div
              className={`alert-card ${
                latestAlert.prediction === "Fraud" ? "danger" : "safe"
              }`}
            >
              <h3>{latestAlert.prediction}</h3>
              <p>Transaction: {latestAlert.transaction_id}</p>
              <p>Probability: {latestAlert.fraud_probability}</p>
            </div>
          ) : (
            <p className="empty">No alert yet.</p>
          )}

          <h2>Queue Monitoring</h2>

          {queueStatus ? (
            <div className="queue-status">
              <p>Size: {queueStatus.size}</p>
              <p>Front: {queueStatus.front}</p>
              <p>Rear: {queueStatus.rear}</p>
              <p>Full: {queueStatus.is_full ? "Yes" : "No"}</p>
            </div>
          ) : (
            <p className="empty">Queue inactive.</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;