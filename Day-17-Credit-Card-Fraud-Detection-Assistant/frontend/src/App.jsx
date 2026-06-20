import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [stats, setStats] = useState(null);
  const [categories, setCategories] = useState([]);
  const [states, setStates] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    amt: "",
    category: "",
    state: "",
    gender: "M"
  });

  useEffect(() => {
    fetch(`${API_URL}/stats`)
      .then((res) => res.json())
      .then((data) => setStats(data));

    fetch(`${API_URL}/categories`)
      .then((res) => res.json())
      .then((data) => {
        setCategories(data);
        if (data.length > 0) {
          setFormData((prev) => ({
            ...prev,
            category: data[0].category
          }));
        }
      });

    fetch(`${API_URL}/states`)
      .then((res) => res.json())
      .then((data) => {
        setStates(data);
        if (data.length > 0) {
          setFormData((prev) => ({
            ...prev,
            state: data[0].state
          }));
        }
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: name === "amt" ? Number(value) : value
    });
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      ...formData
    };

    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">🛡️</div>
          <div>
            <h2>FRAUD</h2>
            <h2>DETECTION</h2>
          </div>
        </div>

        <nav className="nav">
          <a className="nav-item active">🏠 Dashboard</a>
          <a className="nav-item">🔍 Check Transaction</a>
          <a className="nav-item">📊 Statistics</a>
          <a className="nav-item">🏷️ Top Categories</a>
          <a className="nav-item">🛡️ Top States</a>
          <a className="nav-item">🚨 Fraud Samples</a>
          <a className="nav-item">ℹ️ About Project</a>
        </nav>

        <div className="about-card">
          <h3>About</h3>
          <p>
            This system uses K-Nearest Neighbors and Manual Min Heap to predict
            fraud risk and find similar past transactions.
          </p>
          <div className="about-shield">🛡️</div>
        </div>
      </aside>

      <main className="content">
        <header className="top-header">
          <div className="title-block">
            <div className="title-icon">🛡️</div>
            <div>
              <h1>Credit Card Fraud Detection Assistant</h1>
              <p>KNN Model + Manual Min Heap Similarity Search</p>
            </div>
          </div>

          <div className="profile">
            <span>{new Date().toLocaleDateString()} | {new Date().toLocaleTimeString()}</span>
            <div className="avatar">👤</div>
          </div>
        </header>

        <section className="kpi-grid">
          <div className="kpi-card">
            <div className="kpi-icon blue">▤</div>
            <div>
              <p>Total Transactions</p>
              <h2>{stats ? stats.total_transactions.toLocaleString() : "--"}</h2>
              <span>All records in dataset</span>
            </div>
          </div>

          <div className="kpi-card">
            <div className="kpi-icon red">!</div>
            <div>
              <p>Fraud Transactions</p>
              <h2 className="red-text">
                {stats ? stats.fraud_transactions.toLocaleString() : "--"}
              </h2>
              <span>Fraudulent transactions</span>
            </div>
          </div>

          <div className="kpi-card">
            <div className="kpi-icon green">✓</div>
            <div>
              <p>Genuine Transactions</p>
              <h2 className="green-text">
                {stats ? stats.genuine_transactions.toLocaleString() : "--"}
              </h2>
              <span>Legitimate transactions</span>
            </div>
          </div>

          <div className="kpi-card">
            <div className="kpi-icon orange">◔</div>
            <div>
              <p>Fraud Rate</p>
              <h2 className="orange-text">{stats ? `${stats.fraud_rate}%` : "--"}</h2>
              <span>Overall fraud percentage</span>
            </div>
          </div>
        </section>

        <section className="main-grid">
          <form className="panel form-panel" onSubmit={handlePredict}>
            <h2>💳 Check Transaction Risk</h2>

            <label>Transaction Amount (USD)</label>
            <div className="input-box">
              <span>$</span>
              <input
                type="number"
                name="amt"
                placeholder="Enter amount"
                value={formData.amt}
                onChange={handleChange}
                required
              />
            </div>

            <label>Merchant Category</label>
            <div className="input-box">
              <span>🏷️</span>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                required
              >
                {categories.map((item) => (
                  <option key={item.category} value={item.category}>
                    {item.category}
                  </option>
                ))}
              </select>
            </div>

            <label>State / Location</label>
            <div className="input-box">
              <span>📍</span>
              <select name="state" value={formData.state} onChange={handleChange} required>
                {states.map((item) => (
                  <option key={item.state} value={item.state}>
                    {item.state}
                  </option>
                ))}
              </select>
            </div>

            <label>Gender</label>
            <div className="input-box">
              <span>👤</span>
              <select name="gender" value={formData.gender} onChange={handleChange}>
                <option value="M">Male</option>
                <option value="F">Female</option>
              </select>
            </div>

            <button type="submit" disabled={loading}>
              🔍 {loading ? "Checking..." : "Predict Fraud Risk"}
            </button>
          </form>

          <section className="panel result-panel">
            <h2>📈 Prediction Result</h2>

            {!result ? (
              <div className="empty-result">
                <h3>Submit a transaction</h3>
                <p>Prediction result will appear here.</p>
              </div>
            ) : (
              <div className={result.prediction === "Fraud" ? "risk-card fraud-risk" : "risk-card genuine-risk"}>
                <div className="big-shield">
                  {result.prediction === "Fraud" ? "!" : "✓"}
                </div>

                <div className="risk-title-row">
                  <h1>{result.prediction} Transaction</h1>
                  <span>{result.risk_level}</span>
                </div>

                <div className="risk-stats">
                  <div>
                    <p>Fraud Probability</p>
                    <h2>{result.fraud_probability}%</h2>
                  </div>
                  <div>
                    <p>Risk Level</p>
                    <h2>{result.risk_level}</h2>
                  </div>
                </div>

                <p className="risk-message">
                  {result.prediction === "Fraud"
                    ? "This transaction looks suspicious."
                    : "This transaction is likely to be genuine."}
                </p>
              </div>
            )}
          </section>
        </section>

        {result && (
          <section className="panel table-panel">
            <h2>👥 Top 5 Most Similar Past Transactions (Using Manual Min Heap)</h2>

            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Similarity Score</th>
                  <th>Amount (USD)</th>
                  <th>Category</th>
                  <th>State</th>
                  <th>Gender</th>
                  <th>Result</th>
                </tr>
              </thead>

              <tbody>
                {result.similar_transactions.map((item, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td className={item.similarity_score > 0.35 ? "score-red" : "score-green"}>
                      {item.similarity_score}
                    </td>
                    <td>{item.amount}</td>
                    <td>{item.category}</td>
                    <td>{item.state}</td>
                    <td>{item.gender}</td>
                    <td>
                      <span className={item.result === "Fraud" ? "badge fraud-badge" : "badge genuine-badge"}>
                        {item.result === "Fraud" ? "🚨 Fraud" : "✅ Genuine"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;