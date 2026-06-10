import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const emptyForm = {
  patient_id: "",
  name: "",
  age: "",
  heart_rate: "",
  blood_pressure: "",
  oxygen_level: "",
  temperature: "",
};

function App() {
  const [formData, setFormData] = useState(emptyForm);
  const [queueStatus, setQueueStatus] = useState({
    capacity: 5,
    size: 0,
    front: -1,
    rear: -1,
    raw_queue: [],
    critical_patients: 0,
    normal_patients: 0,
  });

  const [dashboard, setDashboard] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [message, setMessage] = useState("");
  const [apiError, setApiError] = useState("");

  const safeRequest = async (url, options = {}) => {
    try {
      const res = await fetch(url, options);
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "API request failed");
      }

      setApiError("");
      return data;
    } catch (error) {
      setApiError(error.message || "Backend connection failed");
      return null;
    }
  };

  const refreshData = async () => {
    const queue = await safeRequest(`${API_URL}/queue_status`);
    const dash = await safeRequest(`${API_URL}/dashboard`);

    if (queue) setQueueStatus(queue);
    if (dash) setDashboard(dash);
  };

  useEffect(() => {
    refreshData();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validateForm = () => {
    if (!formData.patient_id || !formData.name) {
      return "Patient ID and Name are required.";
    }

    const numericFields = [
      "age",
      "heart_rate",
      "blood_pressure",
      "oxygen_level",
      "temperature",
    ];

    for (let field of numericFields) {
      if (formData[field] === "" || isNaN(Number(formData[field]))) {
        return `${field.replace("_", " ")} must be a valid number.`;
      }
    }

    return "";
  };

  const addPatient = async () => {
    const validationError = validateForm();

    if (validationError) {
      setApiError(validationError);
      return;
    }

    const payload = {
      patient_id: formData.patient_id,
      name: formData.name,
      age: Number(formData.age),
      heart_rate: Number(formData.heart_rate),
      blood_pressure: Number(formData.blood_pressure),
      oxygen_level: Number(formData.oxygen_level),
      temperature: Number(formData.temperature),
    };

    const data = await safeRequest(`${API_URL}/add_patient`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!data) return;

    setPrediction(data.patient);
    setMessage(data.message);
    setQueueStatus(data.queue_status);
    setFormData(emptyForm);
    await refreshData();
  };

  const attendPatient = async () => {
    const data = await safeRequest(`${API_URL}/attend_patient`, {
      method: "POST",
    });

    if (!data) return;

    setMessage(data.message);
    setPrediction(data.attended_patient);
    setQueueStatus(data.queue_status);
    await refreshData();
  };

  const viewNextPatient = async () => {
    const data = await safeRequest(`${API_URL}/next_patient`);

    if (!data) return;

    setPrediction(data.next_patient);
    setQueueStatus(data.queue_status);
    setMessage(
      data.next_patient
        ? `Next patient is ${data.next_patient.name}`
        : "No patient waiting"
    );
  };

  const clearForm = () => {
    setFormData(emptyForm);
    setPrediction(null);
    setMessage("");
    setApiError("");
  };

  const queueSlots = Array.from({ length: queueStatus.capacity || 5 }, (_, i) => {
    return queueStatus.raw_queue?.[i] || null;
  });

  const probabilityPercent =
    prediction && prediction.critical_probability !== undefined
      ? Math.round(prediction.critical_probability * 100)
      : 0;

  return (
    <div className="app">
      <header className="topbar">
        <div className="logo">✚</div>
        <h1>Hospital Emergency Triage System</h1>
        <div className="doctor">🕒 Doctor View</div>
      </header>

      <main className="layout">
        <section className="left-panel">
          <div className="card patient-form-card">
            <h2>1. New Patient</h2>

            <label>Patient ID</label>
            <input name="patient_id" value={formData.patient_id} onChange={handleChange} />

            <label>Name</label>
            <input name="name" value={formData.name} onChange={handleChange} />

            <label>Age</label>
            <input name="age" value={formData.age} onChange={handleChange} />

            <label>Heart Rate</label>
            <input name="heart_rate" value={formData.heart_rate} onChange={handleChange} />

            <label>Blood Pressure</label>
            <input name="blood_pressure" value={formData.blood_pressure} onChange={handleChange} />

            <label>Oxygen Level</label>
            <input name="oxygen_level" value={formData.oxygen_level} onChange={handleChange} />

            <label>Temperature</label>
            <input name="temperature" value={formData.temperature} onChange={handleChange} />

            <div className="button-row">
              <button className="add-btn" onClick={addPatient}>+ Add Patient</button>
              <button className="clear-btn" onClick={clearForm}>Clear</button>
            </div>

            {message && <div className="message-box success">{message}</div>}
            {apiError && <div className="message-box error">{apiError}</div>}
          </div>

          <div className="card operations">
            <h2>2. Queue Operations</h2>
            <button className="attend-btn" onClick={attendPatient}>
              Attend Next Patient
            </button>
            <button className="view-btn" onClick={viewNextPatient}>
              View Next Patient
            </button>
          </div>
        </section>

        <section className="center-panel">
          <div className="queue-card">
            <h2>3. Patient Queue Circular Queue</h2>

            <div className="queue-area">
              {queueSlots.map((patient, index) => (
                <div
                  key={index}
                  className={`patient-card ${
                    patient
                      ? patient.prediction === "Critical"
                        ? "critical"
                        : "normal"
                      : "empty"
                  }`}
                >
                  <span className="index">{index}</span>

                  {patient ? (
                    <>
                      <strong>{patient.patient_id}</strong>
                      <p>{patient.name}</p>
                      <b>{patient.prediction}</b>
                    </>
                  ) : (
                    <strong>Empty</strong>
                  )}
                </div>
              ))}
            </div>

            <div className="queue-meta">
              <span>Front: {queueStatus.front}</span>
              <span>Rear: {queueStatus.rear}</span>
              <span>Size: {queueStatus.size}</span>
              <span>Capacity: {queueStatus.capacity}</span>
            </div>

            <div className="hospital-scene">
              <div className="scene-box">
                <h3>Reception</h3>
                <div className="person">👩‍💼</div>
                <div className="desk"></div>
              </div>

              <div className="scene-box">
                <h3 className="emergency-title">Emergency</h3>
                <div className="bed">🛏️</div>
              </div>

              <div className="scene-box">
                <h3 className="doctor-title">Doctor / ICU</h3>
                <div className="person">👨‍⚕️</div>
              </div>
            </div>

            <div className="legend">
              <span><i className="box red"></i> Critical Patient</span>
              <span><i className="box green"></i> Normal Patient</span>
              <span><i className="box empty-box"></i> Empty Slot</span>
            </div>
          </div>
        </section>

        <section className="right-panel">
          <div className="card prediction">
            <h2>4. AI Prediction</h2>

            {prediction ? (
              <>
                <p><strong>Patient ID:</strong> {prediction.patient_id}</p>
                <p><strong>Name:</strong> {prediction.name}</p>

                <h3>Prediction</h3>

                <div className={prediction.prediction === "Critical" ? "critical-text" : "normal-text"}>
                  {prediction.prediction}
                </div>

                <p><strong>Critical Probability:</strong></p>
                <div className="probability">
                  {prediction.critical_probability} ({probabilityPercent}%)
                </div>

                <div className="bar">
                  <div
                    className={prediction.prediction === "Critical" ? "bar-fill critical-fill" : "bar-fill"}
                    style={{ width: `${probabilityPercent}%` }}
                  ></div>
                </div>
              </>
            ) : (
              <div className="empty-prediction">
                Add or select a patient to view AI prediction.
              </div>
            )}
          </div>

          <div className="card dashboard">
            <h2>5. Dashboard</h2>

            <div className="stats">
              <div className="stat blue">
                <p>Total Waiting</p>
                <strong>{dashboard?.total_patients_waiting || 0}</strong>
              </div>

              <div className="stat red-stat">
                <p>Critical</p>
                <strong>{dashboard?.critical_patients || 0}</strong>
              </div>

              <div className="stat green-stat">
                <p>Normal</p>
                <strong>{dashboard?.normal_patients || 0}</strong>
              </div>

              <div className="stat yellow">
                <p>Capacity</p>
                <strong>{queueStatus.capacity || 5}</strong>
              </div>
            </div>

            <div className="next-box">
              <p>Next Patient</p>

              {dashboard?.next_patient ? (
                <>
                  <strong>
                    {dashboard.next_patient.patient_id} - {dashboard.next_patient.name}
                  </strong>
                  <span>{dashboard.next_patient.prediction}</span>
                </>
              ) : (
                <strong>No patient waiting</strong>
              )}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;