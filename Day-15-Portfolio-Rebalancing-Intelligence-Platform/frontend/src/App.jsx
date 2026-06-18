import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [tickers, setTickers] = useState("AAPL, TSLA, NVDA, JPM");
  const [analysis, setAnalysis] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [stackHistory, setStackHistory] = useState([]);
  const [highestRisk, setHighestRisk] = useState(null);

  const API_URL = "http://127.0.0.1:8000";

  const getTickerList = () =>
    tickers
      .split(",")
      .map((ticker) => ticker.trim().toUpperCase())
      .filter(Boolean);

  const analyzePortfolio = async () => {
    const response = await axios.post(`${API_URL}/analyze-portfolio`, {
      tickers: getTickerList(),
    });

    const sorted = [...response.data.portfolio_analysis].sort(
      (a, b) => b.risk_score - a.risk_score
    );

    setAnalysis(sorted);
    setHighestRisk(response.data.highest_risk_asset);
  };

  const rebalancePortfolio = async () => {
    const response = await axios.post(`${API_URL}/rebalance-portfolio`, {
      tickers: getTickerList(),
    });

    setRecommendations(response.data.recommendations);
    setStackHistory(response.data.stack_history);
  };

  const undoChange = async () => {
    const response = await axios.delete(`${API_URL}/undo-change`);
    setStackHistory(response.data.remaining_changes);
  };

  const highCount = analysis.filter((item) => item.predicted_risk === "High Risk").length;
  const mediumCount = analysis.filter((item) => item.predicted_risk === "Medium Risk").length;
  const lowCount = analysis.filter((item) => item.predicted_risk === "Low Risk").length;

  const riskClass = (risk) => {
    if (risk === "High Risk") return "high";
    if (risk === "Medium Risk") return "medium";
    return "low";
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">📈</div>
          <div>
            <h2>Portfolio Rebalancing</h2>
            <p>Intelligence Platform</p>
          </div>
        </div>

        <nav>
          <button className="active">▦ Dashboard</button>
          <button>▥ Portfolio Analysis</button>
          <button>⚖ Rebalance Actions</button>
          <button>♛ Risk Ranking</button>
          <button>↶ History Stack</button>
          <button>⚙ Settings</button>
          <button>🛡 Permissions</button>
          <button>👥 Users</button>
        </nav>

        <div className="system-card">
          <h3>System Status</h3>
          <p><span className="dot"></span> All Systems Operational</p>
          <div className="status-row"><span>Model</span><b>Active</b></div>
          <div className="status-row"><span>Data Source</span><b>Connected</b></div>
          <div className="status-row"><span>Last Updated</span><b>10:24 AM</b></div>
        </div>
      </aside>

      <main className="main">
        <header className="header">
          <div>
            <h1>Portfolio Rebalancing Intelligence Platform</h1>
            <p>XGBoost Risk Prediction • Stack Undo • Priority Queue Ranking</p>
          </div>
          <div className="profile">
            <div className="avatar">PM</div>
            <div>
              <strong>Pranit Mhatre</strong>
              <span>Admin</span>
            </div>
          </div>
        </header>

        <section className="input-panel">
          <input
            value={tickers}
            onChange={(e) => setTickers(e.target.value)}
            placeholder="Enter tickers comma separated"
          />
          <button onClick={analyzePortfolio}>📊 Analyze Portfolio</button>
          <button className="purple" onClick={rebalancePortfolio}>⚖ Rebalance Portfolio</button>
          <button className="teal" onClick={undoChange}>↶ Undo Last Change</button>
        </section>

        <section className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon blue">◔</div>
            <div><p>Total Assets</p><h2>{analysis.length}</h2><span>In Portfolio</span></div>
          </div>
          <div className="stat-card">
            <div className="stat-icon red">!</div>
            <div><p>High Risk Assets</p><h2>{highCount}</h2><span className="red-text">{analysis.length ? ((highCount / analysis.length) * 100).toFixed(0) : 0}%</span></div>
          </div>
          <div className="stat-card">
            <div className="stat-icon orange">▲</div>
            <div><p>Medium Risk Assets</p><h2>{mediumCount}</h2><span className="orange-text">{analysis.length ? ((mediumCount / analysis.length) * 100).toFixed(0) : 0}%</span></div>
          </div>
          <div className="stat-card">
            <div className="stat-icon green">✓</div>
            <div><p>Low Risk Assets</p><h2>{lowCount}</h2><span className="green-text">{analysis.length ? ((lowCount / analysis.length) * 100).toFixed(0) : 0}%</span></div>
          </div>
          <div className="stat-card">
            <div className="stat-icon violet">♛</div>
            <div><p>Highest Risk Asset</p><h2 className="violet-text">{highestRisk?.ticker || "N/A"}</h2><span>Score: {highestRisk?.risk_score || 0}/100</span></div>
          </div>
        </section>

        <section className="content-grid">
          <div className="panel">
            <h3>Risk Distribution</h3>
            <div className="donut">
              <div className="hole"></div>
            </div>
            <div className="legend"><span className="box red-box"></span> High Risk ({highCount})</div>
            <div className="legend"><span className="box orange-box"></span> Medium Risk ({mediumCount})</div>
            <div className="legend"><span className="box green-box"></span> Low Risk ({lowCount})</div>
          </div>

          <div className="panel">
            <h3>Risk Ranking <small>(Priority Queue)</small></h3>
            {analysis.map((item, index) => (
              <div className="rank-row" key={item.ticker}>
                <span className="rank-no">{index + 1}</span>
                <strong>{item.ticker}</strong>
                <span className={`badge ${riskClass(item.predicted_risk)}`}>{item.predicted_risk}</span>
                <b>{item.risk_score}</b>
                <div className="bar"><div className={riskClass(item.predicted_risk)} style={{ width: `${item.risk_score}%` }}></div></div>
              </div>
            ))}
          </div>

          <div className="panel">
            <h3>Rebalance Actions <small>(Stack)</small></h3>
            {recommendations.map((item, index) => (
              <div className={`action ${riskClass(item.risk)}`} key={index}>
                <div>
                  <strong>{item.action}</strong>
                  <p>{item.reason}</p>
                </div>
                <span className={`badge ${riskClass(item.risk)}`}>{item.risk}</span>
              </div>
            ))}
          </div>

          <div className="panel">
            <h3>Stack History <small>(Undo)</small></h3>
            {stackHistory.map((item, index) => (
              <div className="history" key={index}>
                <span>{stackHistory.length - index}</span>
                <p>{item.action}</p>
                <small>10:24 AM</small>
              </div>
            ))}
          </div>
        </section>

        <section className="table-panel">
          <h3>Portfolio Analysis</h3>
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Ticker</th>
                <th>Average Return</th>
                <th>Volatility</th>
                <th>Predicted Risk</th>
                <th>Risk Score</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {analysis.map((item, index) => (
                <tr key={item.ticker}>
                  <td>{index + 1}</td>
                  <td><b>{item.ticker}</b></td>
                  <td>{item.average_return}</td>
                  <td>{item.volatility}</td>
                  <td><span className={`badge ${riskClass(item.predicted_risk)}`}>{item.predicted_risk}</span></td>
                  <td>{item.risk_score}</td>
                  <td>{item.predicted_risk === "High Risk" ? "↓ Reduce" : item.predicted_risk === "Medium Risk" ? "— Monitor" : "✓ Hold"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}

export default App;