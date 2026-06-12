import { useState } from "react";
import {
  Brain,
  Home,
  ListChecks,
  Layers,
  Info,
  Plus,
  RotateCcw,
  Clock,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [description, setDescription] = useState("");
  const [lastIncident, setLastIncident] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [action, setAction] = useState("");
  const [actions, setActions] = useState([]);

  const createIncident = async () => {
    if (!description.trim()) return;

    const response = await fetch(`${API_URL}/predict-incident`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ description }),
    });

    const data = await response.json();

    setLastIncident(data.incident);
    setIncidents(data.incidents);
    setDescription("");
  };

  const selectIncident = async (incident) => {
    setSelectedIncident(incident);

    const response = await fetch(`${API_URL}/actions/${incident.id}`);
    const data = await response.json();

    setActions(data.actions);
  };

  const addAction = async () => {
    if (!selectedIncident || !action.trim()) return;

    const response = await fetch(`${API_URL}/add-action`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        incident_id: selectedIncident.id,
        action,
      }),
    });

    const data = await response.json();

    setActions(data.current_stack);
    setAction("");
  };

  const undoAction = async () => {
    if (!selectedIncident) return;

    const response = await fetch(`${API_URL}/undo-action`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        incident_id: selectedIncident.id,
      }),
    });

    const data = await response.json();
    setActions(data.current_stack);
  };

  const getSeverityClass = (severity) => {
    if (severity === "Critical") return "critical";
    if (severity === "High") return "high";
    if (severity === "Medium") return "medium";
    return "low";
  };

  const countSeverity = (severity) => {
    return incidents.filter((incident) => incident.severity === severity).length;
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <Brain size={24} />
        </div>

        <div className="nav active">
          <Home size={20} />
          <span>Dashboard</span>
        </div>

        <div className="nav">
          <ListChecks size={20} />
          <span>Incidents</span>
        </div>

        <div className="nav">
          <Layers size={20} />
          <span>Actions</span>
        </div>

        <div className="nav">
          <Info size={20} />
          <span>About</span>
        </div>
      </aside>

      <main className="main">
        <header className="header">
          <div>
            <h1>AI Incident Management System</h1>
            <p>DSA + AI Powered</p>
          </div>

          <div className="status">
            <span className="online-dot"></span>
            System Online
          </div>
        </header>

        <section className="dashboard">
          <div className="panel">
            <h2>1. Create Incident</h2>

            <label>Describe the incident</label>
            <textarea
              value={description}
              maxLength={200}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Example: Database crashed after deployment"
            />
            <div className="char-count">{description.length}/200</div>

            <button className="primary-btn" onClick={createIncident}>
              <Brain size={16} />
              Predict Incident
            </button>

            <div className="result-box">
              <h3>AI Prediction Result</h3>

              {lastIncident ? (
                <>
                  <div className="result-row">
                    <span>Category</span>
                    <strong>{lastIncident.category}</strong>
                  </div>
                  <div className="result-row">
                    <span>Severity</span>
                    <b className={`badge ${getSeverityClass(lastIncident.severity)}`}>
                      {lastIncident.severity}
                    </b>
                  </div>
                  <div className="result-row">
                    <span>Incident ID</span>
                    <strong>#{lastIncident.id}</strong>
                  </div>
                </>
              ) : (
                <p className="empty">No incident predicted yet.</p>
              )}
            </div>

            <div className="flow-box">
              <h3>How it works?</h3>
              <div className="flow">
                <span>Naive Bayes</span>
                <span>→</span>
                <span>Severity</span>
                <span>→</span>
                <span>Queue</span>
              </div>
            </div>
          </div>

          <div className="panel center-panel">
            <h2>2. Priority Queue</h2>

            <div className="filters">
              <span>All {incidents.length}</span>
              <span className="critical">Critical {countSeverity("Critical")}</span>
              <span className="high">High {countSeverity("High")}</span>
              <span className="medium">Medium {countSeverity("Medium")}</span>
              <span className="low">Low {countSeverity("Low")}</span>
            </div>

            <div className="incident-list">
              {incidents.length === 0 ? (
                <p className="empty">No incidents added yet.</p>
              ) : (
                incidents.map((incident) => (
                  <div
                    className={`incident-card ${getSeverityClass(incident.severity)}`}
                    key={incident.id}
                    onClick={() => selectIncident(incident)}
                  >
                    <div className="incident-top">
                      <strong>#{incident.id} {incident.category}</strong>
                      <b className={`badge ${getSeverityClass(incident.severity)}`}>
                        {incident.severity}
                      </b>
                    </div>
                    <p>{incident.description}</p>
                    <div className="incident-meta">
                      <Clock size={12} />
                      <span>Status: {incident.status}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="panel">
            <h2>3. Troubleshooting Stack</h2>

            <div className="selected-box">
              <h3>Selected Incident</h3>

              {selectedIncident ? (
                <>
                  <p>ID: #{selectedIncident.id}</p>
                  <p>Category: {selectedIncident.category}</p>
                  <p>Severity: {selectedIncident.severity}</p>
                  <p>Description: {selectedIncident.description}</p>
                </>
              ) : (
                <p className="empty">Select an incident from queue.</p>
              )}
            </div>

            <div className="action-box">
              <label>Add Action</label>
              <input
                value={action}
                onChange={(e) => setAction(e.target.value)}
                placeholder="Example: Checked database logs"
              />

              <button className="green-btn" onClick={addAction}>
                <Plus size={16} />
                Add Action
              </button>
            </div>

            <div className="stack-box">
              <div className="stack-header">
                <h3>Action History</h3>
                <button className="undo-btn" onClick={undoAction}>
                  <RotateCcw size={14} />
                  Undo
                </button>
              </div>

              <div className="stack-list">
                {actions.length === 0 ? (
                  <p className="empty">No actions added.</p>
                ) : (
                  [...actions].reverse().map((item, index) => (
                    <div className="stack-item" key={index}>
                      <span>{actions.length - index}</span>
                      <p>{item}</p>
                      {index === 0 && <small>Latest</small>}
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </section>

        <footer className="footer">
          Priority Queue handles incident order. Stack stores troubleshooting actions using LIFO.
        </footer>
      </main>
    </div>
  );
}

export default App;