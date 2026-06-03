import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [title, setTitle] = useState("Checkout Failure");
  const [description, setDescription] = useState(
    "Transaction service unexpectedly terminates when checkout starts"
  );

  const [queue, setQueue] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [latestPrediction, setLatestPrediction] = useState(null);
  const [message, setMessage] = useState("");
  const [assignMessage, setAssignMessage] = useState("");

  const fetchQueue = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/queue`);
      setQueue(response.data.queue || []);
    } catch (error) {
      console.error("Error fetching queue:", error);
      setAssignMessage("Unable to refresh queue. Please check backend.");
    }
  };

  const fetchMetrics = async () => {
    const response = await axios.get(`${API_BASE_URL}/model-metrics`);
    setMetrics(response.data);
  };

  const submitBug = async (e) => {
    e.preventDefault();

    const response = await axios.post(`${API_BASE_URL}/add-bug`, {
      title,
      description,
    });

    setLatestPrediction(response.data);
    setQueue(response.data.current_queue || []);
    setMessage(
      `Predicted Priority: ${response.data.priority_label} (${response.data.priority_number})`
    );

    setAssignMessage("");
  };

  const assignTask = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/next-bug`);
      const assignedBug = response.data.next_bug;
  
      if (!assignedBug) {
        setAssignMessage("No bug available in queue to assign.");
        return;
      }
  
      setAssignMessage(
        `${assignedBug.priority_label} bug "${assignedBug.bug_title}" assigned to respective developer/team. Proceed!`
      );
  
      fetchQueue();
    } catch (error) {
      console.error("Error assigning bug:", error);
      setAssignMessage("Unable to assign bug. Please check backend.");
    }
  };

  useEffect(() => {
    fetchQueue();
    fetchMetrics();
  }, []);

  return (
    <div className="app">
      <header className="top-header">
        <div className="brand">
          <span className="bug-icon">🐞</span>
          <h1>AI Bug Ticket Priority Classifier</h1>
        </div>
        <div className="project-badge">🧠 AI + DSA Project</div>
      </header>

      <main className="dashboard">
        <section className="left-panel">
          <div className="card form-card">
            <div className="card-title">
              <span>📄</span>
              <h2>Submit New Bug</h2>
            </div>

            <form onSubmit={submitBug}>
              <label>Bug Title</label>
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter bug title"
              />

              <label>Bug Description</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe the bug"
              />

              <button className="submit-btn" type="submit">
                🚀 Submit Bug
              </button>
            </form>

            {message && (
              <div className="success-box">
                <span>✅</span>
                <div>
                  <strong>{message}</strong>
                  <p>Bug added to priority queue successfully!</p>
                </div>
              </div>
            )}
          </div>

          <div className="card prediction-card">
            <div className="card-title">
              <span>🕒</span>
              <h2>Latest Prediction</h2>
            </div>

            {latestPrediction ? (
              <div className="prediction-details">
                <p>
                  <strong>Title:</strong>
                  <span>{latestPrediction.title}</span>
                </p>
                <p>
                  <strong>Description:</strong>
                  <span>{latestPrediction.description}</span>
                </p>
                <hr />
                <p>
                  <strong>Predicted Priority:</strong>
                  <span className={`pill ${latestPrediction.priority_label}`}>
                    {latestPrediction.priority_label} (
                    {latestPrediction.priority_number})
                  </span>
                </p>
                <p>
                  <strong>Status:</strong>
                  <span className="status-pill">Added to Queue</span>
                </p>
              </div>
            ) : (
              <p className="empty-text">Submit a bug to see prediction.</p>
            )}
          </div>
        </section>

        <section className="right-panel">
          <div className="card metrics-card">
            <div className="card-title">
              <span>📊</span>
              <h2>AI Model Performance</h2>
            </div>

            <div className="metrics-grid">
              <div className="metric metric-purple">
                <p>Accuracy</p>
                <h3>{metrics ? `${metrics.accuracy}%` : "--"}</h3>
                <span>◎</span>
              </div>

              <div className="metric metric-green">
                <p>Precision</p>
                <h3>{metrics ? `${metrics.precision}%` : "--"}</h3>
                <span>◉</span>
              </div>

              <div className="metric metric-blue">
                <p>Recall</p>
                <h3>{metrics ? `${metrics.recall}%` : "--"}</h3>
                <span>⌖</span>
              </div>

              <div className="metric metric-yellow">
                <p>F1 Score</p>
                <h3>{metrics ? `${metrics.f1_score}%` : "--"}</h3>
                <span>☆</span>
              </div>
            </div>

            <p className="metric-note">
              Model evaluated on test data using TF-IDF + Naive Bayes.
            </p>
          </div>

          <div className="card queue-card">
            <div className="queue-header">
              <div className="card-title">
                <span>☷</span>
                <h2>Priority Queue (Bug Tickets)</h2>
              </div>

              <div className="queue-actions">
                <button type="button" className="outline-btn" onClick={fetchQueue}>
                  ↻ Refresh
                </button>
                <button type="button" className="assign-btn" onClick={assignTask}>
                  👥 Assign Task
                </button>
              </div>
            </div>

            {assignMessage && (
              <div className="assign-alert">
                ✅ {assignMessage}
              </div>
            )}

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Priority</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>
                  {queue.length > 0 ? (
                    queue.map((bug, index) => (
                      <tr key={index}>
                        <td>
                          <span className={`priority-number ${bug.priority_label}`}>
                            {bug.priority_number}
                          </span>
                          <span className={`priority-text ${bug.priority_label}`}>
                            {bug.priority_label}
                          </span>
                        </td>
                        <td>{bug.bug_title}</td>
                        <td className="description-cell">
                          {bug.bug_description}
                        </td>
                        <td>
                          <span className="status-pill">In Queue</span>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="4" className="empty-row">
                        No bugs in queue yet.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <p className="queue-note">
              Top of the queue has the highest priority bug.
            </p>
          </div>
        </section>
      </main>

      <footer>Built with ❤️ using FastAPI, React, and Machine Learning</footer>
    </div>
  );
}

export default App;