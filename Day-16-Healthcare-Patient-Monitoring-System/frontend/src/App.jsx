import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const emptyForm = {
  timestamp: "",
  heart_rate: "",
  spo2: "",
  respiratory_rate: "",
  systolic_bp: "",
  diastolic_bp: "",
  temperature: "",
};

function App() {
  const [patient, setPatient] = useState(null);
  const [latestReading, setLatestReading] = useState(null);
  const [history, setHistory] = useState([]);
  const [events, setEvents] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [formData, setFormData] = useState(emptyForm);

  const loadDashboard = async () => {
    try {
      const patientRes = await axios.get(`${API_URL}/patient`);
      const latestRes = await axios.get(`${API_URL}/readings/latest`);
      const historyRes = await axios.get(`${API_URL}/readings/history`);
      const eventsRes = await axios.get(`${API_URL}/events/history`);

      setPatient(patientRes.data);
      setLatestReading(latestRes.data);
      setHistory(Array.isArray(historyRes.data) ? historyRes.data : []);
      setEvents(eventsRes.data.events || []);
    } catch (error) {
      console.error("API loading error:", error);
    }
  };

  const handleInputChange = (key, value) => {
    setFormData({
      ...formData,
      [key]: value,
    });
  };

  const addReading = async () => {
    const payload = {
      timestamp: formData.timestamp,
      heart_rate: Number(formData.heart_rate),
      spo2: Number(formData.spo2),
      respiratory_rate: Number(formData.respiratory_rate),
      systolic_bp: Number(formData.systolic_bp),
      diastolic_bp: Number(formData.diastolic_bp),
      temperature: Number(formData.temperature),
    };

    await axios.post(`${API_URL}/readings`, payload);
    setFormData(emptyForm);
    setPrediction(null);
    await loadDashboard();
  };

  const predictHeartRate = async () => {
    const res = await axios.get(`${API_URL}/predict/heart-rate`);
    setPrediction(res.data);
    await loadDashboard();
  };

  const undoReading = async () => {
    await axios.delete(`${API_URL}/readings/undo`);
    setPrediction(null);
    await loadDashboard();
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const hasLatestReading = latestReading && latestReading.timestamp;

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">+</div>
          <div>
            <h1>Healthcare Patient Monitoring System</h1>
            <p>Stack based vital history with SVR heart rate prediction</p>
          </div>
        </div>

        <div className="api-pill">API Connected</div>
      </header>

      <main className="layout">
        <section className="card patient-card">
          <div className="card-header">
            <h2>Patient Details</h2>
          </div>

          {patient ? (
            <div className="patient-box">
              <div className="avatar">
                {patient.gender ? patient.gender.charAt(0).toUpperCase() : "P"}
              </div>

              <div className="patient-data">
                <p><span>Patient ID</span><b>{patient.patient_id}</b></p>
                <p><span>Age</span><b>{patient.age}</b></p>
                <p><span>Gender</span><b>{patient.gender}</b></p>
                <p><span>Diagnosis</span><b>{patient.diagnosis}</b></p>
                <p><span>Admission</span><b>{patient.admission_type}</b></p>
                <p><span>Comorbidity</span><b>{patient.comorbidity_count}</b></p>
              </div>
            </div>
          ) : (
            <div className="empty">No patient data</div>
          )}
        </section>

        <section className="card latest-card">
          <div className="card-header">
            <h2>Latest Vital Reading</h2>
            {hasLatestReading && <small>{latestReading.timestamp}</small>}
          </div>

          {hasLatestReading ? (
            <>
              <div className="vitals">
                <div className="vital-box">
                  <span>Heart Rate</span>
                  <b>{latestReading.heart_rate}</b>
                  <small>BPM</small>
                </div>

                <div className="vital-box">
                  <span>SpO2</span>
                  <b>{latestReading.spo2}</b>
                  <small>%</small>
                </div>

                <div className="vital-box">
                  <span>Resp Rate</span>
                  <b>{latestReading.respiratory_rate}</b>
                  <small>/min</small>
                </div>

                <div className="vital-box">
                  <span>Blood Pressure</span>
                  <b>{latestReading.systolic_bp}/{latestReading.diastolic_bp}</b>
                  <small>mmHg</small>
                </div>

                <div className="vital-box">
                  <span>Temperature</span>
                  <b>{latestReading.temperature}</b>
                  <small>°C</small>
                </div>
              </div>

              <div className="action-row">
                <button onClick={predictHeartRate}>Predict Heart Rate</button>
                <button className="success" onClick={undoReading}>Undo Latest</button>
              </div>
            </>
          ) : (
            <div className="empty">No latest reading available</div>
          )}
        </section>

        <section className="card stack-card">
          <div className="card-header">
            <h2>Reading Stack History</h2>
            <small>{history.length} readings</small>
          </div>

          <div className="scroll-list">
            {history.length === 0 ? (
              <div className="empty">Stack is empty</div>
            ) : (
              history.map((item, index) => (
                <div className="stack-item" key={index}>
                  <div className="stack-index">{history.length - index}</div>
                  <div>
                    <p><b>{item.timestamp}</b></p>
                    <p>HR {item.heart_rate} BPM · SpO2 {item.spo2}% · RR {item.respiratory_rate}</p>
                    <p>BP {item.systolic_bp}/{item.diastolic_bp} · Temp {item.temperature} °C</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>

        <section className="card form-card">
          <div className="card-header">
            <h2>Add New Vital Reading</h2>
          </div>

          <div className="form-list">
            {Object.keys(formData).map((key) => (
              <div className="form-row" key={key}>
                <label>{key.replaceAll("_", " ")}</label>
                <input
                  type={key === "timestamp" ? "text" : "number"}
                  value={formData[key]}
                  placeholder={key.replaceAll("_", " ")}
                  onChange={(e) => handleInputChange(key, e.target.value)}
                />
              </div>
            ))}
          </div>

          <button className="add-button" onClick={addReading}>Add Reading</button>
        </section>

        <section className="card event-card">
          <div className="card-header">
            <h2>Medical Event Timeline</h2>
            <small>{events.length} events</small>
          </div>

          <div className="scroll-list">
            {events.length === 0 ? (
              <div className="empty">No events available</div>
            ) : (
              events.map((event, index) => (
                <div className="event-item" key={index}>
                  <div className="dot"></div>
                  <p>{event}</p>
                </div>
              ))
            )}
          </div>
        </section>

        <section className="card prediction-card">
          <div className="card-header">
            <h2>SVR Heart Rate Prediction</h2>
          </div>

          {prediction && prediction.predicted_heart_rate ? (
            <div className="prediction-result">
              <span>Predicted Heart Rate</span>
              <b>{prediction.predicted_heart_rate}</b>
              <small>{prediction.unit}</small>
            </div>
          ) : (
            <div className="empty">Prediction appears after clicking Predict Heart Rate</div>
          )}
        </section>

        <section className="card overview-card">
          <div className="card-header">
            <h2>System Overview</h2>
          </div>

          <div className="overview-grid">
            <div>
              <b>{history.length}</b>
              <span>Total Readings</span>
            </div>

            <div>
              <b>{events.length}</b>
              <span>Total Events</span>
            </div>

            <div>
              <b>{prediction?.predicted_heart_rate || "--"}</b>
              <span>Last Prediction</span>
            </div>

            <div>
              <b>{hasLatestReading ? "Active" : "Waiting"}</b>
              <span>Monitor Status</span>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;