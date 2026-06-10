import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    equipment_name: "",
    equipment_type: "",
    equipment_age: "",
    usage_hours: "",
    previous_breakdowns: "",
    maintenance_frequency: "",
    error_count: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [queue, setQueue] = useState([]);
  const [processed, setProcessed] = useState([]);

  const equipmentTypes = [
    "Ventilator",
    "ECG Machine",
    "MRI Scanner",
    "CT Scanner",
    "Patient Monitor",
    "Infusion Pump",
    "Defibrillator",
    "X-Ray Machine",
    "Ultrasound System",
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handlePredict = async (e) => {
    e.preventDefault();

    const payload = {
      equipment_name: formData.equipment_name,
      equipment_type: formData.equipment_type,
      equipment_age: Number(formData.equipment_age),
      usage_hours: Number(formData.usage_hours),
      previous_breakdowns: Number(formData.previous_breakdowns),
      maintenance_frequency: Number(formData.maintenance_frequency),
      error_count: Number(formData.error_count),
    };

    const response = await axios.post(
      "http://127.0.0.1:8000/predict-maintenance",
      payload
    );

    setPrediction(response.data);
    setQueue(response.data.current_queue);
  };

  const processNext = async () => {
    const response = await axios.delete("http://127.0.0.1:8000/process-next");

    if (response.data.processed_request) {
      setProcessed([response.data.processed_request, ...processed]);
    }

    setQueue(response.data.remaining_queue || []);
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo-box">
          <div className="logo-icon">✚</div>
          <h2>Smart Medical Equipment</h2>
        </div>

        <nav>
          <p className="active">⌂ Dashboard</p>
          <p>🩺 Add Equipment</p>
          <p>📋 Maintenance Queue</p>
          <p>✅ Processed Requests</p>
          <p>📊 Analytics</p>
          <p>⚙ Settings</p>
        </nav>

        <div className="hospital-card">
          <div className="hospital-icon">🏥</div>
          <h3>City Care Hospital</h3>
          <p>Biomedical Engineering Dept.</p>
        </div>
      </aside>

      <main className="main-content">
        <header className="top-header">
          <div>
            <h1>Smart Medical Equipment Maintenance System</h1>
            <p>AI-powered predictive maintenance using Logistic Regression + Deque</p>
          </div>

          <div className="admin-box">
            <span className="status-dot"></span>
            System Online
          </div>
        </header>

        <section className="stats-grid">
          <div className="stat-card blue">
            <span>🖥</span>
            <div>
              <h3>{queue.length + processed.length}</h3>
              <p>Total Equipment Checked</p>
            </div>
          </div>

          <div className="stat-card red">
            <span>⚠</span>
            <div>
              <h3>
                {queue.filter((item) => item.prediction === 1).length}
              </h3>
              <p>High Risk Equipment</p>
            </div>
          </div>

          <div className="stat-card orange">
            <span>🛠</span>
            <div>
              <h3>{queue.length}</h3>
              <p>In Maintenance Queue</p>
            </div>
          </div>

          <div className="stat-card green">
            <span>✅</span>
            <div>
              <h3>{processed.length}</h3>
              <p>Processed Requests</p>
            </div>
          </div>
        </section>

        <section className="dashboard-grid">
          <div className="card form-card">
            <h2>🩺 Add Equipment for Analysis</h2>

            <form onSubmit={handlePredict}>
              <label>Equipment Name</label>
              <input
                name="equipment_name"
                value={formData.equipment_name}
                onChange={handleChange}
                placeholder="e.g. Ventilator A1"
                required
              />

              <label>Equipment Type</label>
              <select
                name="equipment_type"
                value={formData.equipment_type}
                onChange={handleChange}
                required
              >
                <option value="">Select Equipment Type</option>
                {equipmentTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>

              <div className="two-col">
                <div>
                  <label>Equipment Age</label>
                  <input
                    name="equipment_age"
                    value={formData.equipment_age}
                    onChange={handleChange}
                    placeholder="e.g. 10"
                    required
                  />
                </div>

                <div>
                  <label>Usage Hours</label>
                  <input
                    name="usage_hours"
                    value={formData.usage_hours}
                    onChange={handleChange}
                    placeholder="e.g. 15000"
                    required
                  />
                </div>
              </div>

              <div className="two-col">
                <div>
                  <label>Previous Breakdowns</label>
                  <input
                    name="previous_breakdowns"
                    value={formData.previous_breakdowns}
                    onChange={handleChange}
                    placeholder="e.g. 6"
                    required
                  />
                </div>

                <div>
                  <label>Maintenance Frequency</label>
                  <input
                    name="maintenance_frequency"
                    value={formData.maintenance_frequency}
                    onChange={handleChange}
                    placeholder="e.g. 120"
                    required
                  />
                </div>
              </div>

              <label>Error Count</label>
              <input
                name="error_count"
                value={formData.error_count}
                onChange={handleChange}
                placeholder="e.g. 50"
                required
              />

              <button type="submit">💓 Predict & Add to Queue</button>
            </form>
          </div>

          <div className="card prediction-card">
            <h2>🧠 AI Prediction Result</h2>

            {prediction ? (
              <>
                <div className="gauge">
                  <h1>{prediction.prediction_result.failure_probability}%</h1>
                  <p>Failure Probability</p>
                </div>

                <div className="result-list">
                  <div>
                    <span>Risk Level</span>
                    <strong>{prediction.risk_level}</strong>
                  </div>

                  <div>
                    <span>Prediction</span>
                    <strong>
                      {prediction.prediction_result.prediction === 1
                        ? "Failure Likely"
                        : "Failure Unlikely"}
                    </strong>
                  </div>

                  <div>
                    <span>Priority</span>
                    <strong>{prediction.priority}</strong>
                  </div>
                </div>

                <p className="info-box">
                  This equipment was added to the{" "}
                  {prediction.priority === "Critical" ? "front" : "rear"} of the
                  maintenance queue.
                </p>
              </>
            ) : (
              <p className="empty-text">
                Add equipment details to view AI prediction.
              </p>
            )}
          </div>

          <div className="card queue-card">
            <div className="queue-header">
              <h2>📋 Maintenance Queue (Deque)</h2>
              <button onClick={processNext}>Process Next</button>
            </div>

            <div className="queue-labels">
              <span>Front: Critical</span>
              <span>Rear: Routine</span>
            </div>

            <div className="queue-list">
              {queue.length === 0 ? (
                <p className="empty-text">No equipment in queue.</p>
              ) : (
                queue.map((item, index) => (
                  <div
                    className={
                      item.prediction === 1
                        ? "equipment-card critical"
                        : "equipment-card routine"
                    }
                    key={index}
                  >
                    <div className="equipment-icon">
                      {item.equipment_type === "Ventilator"
                        ? "🫁"
                        : item.equipment_type === "ECG Machine"
                        ? "📈"
                        : item.equipment_type === "MRI Scanner"
                        ? "🧲"
                        : item.equipment_type === "Patient Monitor"
                        ? "🖥"
                        : "⚕"}
                    </div>

                    <h4>{item.equipment_name}</h4>
                    <p>{item.equipment_type}</p>
                    <strong>{item.failure_probability}%</strong>
                  </div>
                ))
              )}
            </div>

            <div className="concept-box">
              <h3>Deque Concept</h3>
              <p>Critical equipment is inserted at the front.</p>
              <p>Routine equipment is inserted at the rear.</p>
              <p>Processing always happens from the front.</p>
            </div>
          </div>
        </section>

        <section className="bottom-grid">
          <div className="card">
            <h2>✅ Recently Processed</h2>

            {processed.length === 0 ? (
              <p className="empty-text">No processed requests yet.</p>
            ) : (
              processed.map((item, index) => (
                <div className="processed-item" key={index}>
                  <strong>{item.equipment_name}</strong>
                  <span>Completed</span>
                </div>
              ))
            )}
          </div>

          <div className="card">
            <h2>🔍 How It Works</h2>

            <div className="how-box">
              <h3>Machine Learning</h3>
              <p>
                Logistic Regression predicts failure probability using age, usage
                hours, breakdown history, maintenance frequency, and error count.
              </p>
            </div>

            <div className="how-box">
              <h3>Deque Data Structure</h3>
              <p>
                Critical failures are added to the front, while routine requests
                are added to the rear.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;