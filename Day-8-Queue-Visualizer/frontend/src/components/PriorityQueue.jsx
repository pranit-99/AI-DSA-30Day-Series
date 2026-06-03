import { useState } from "react";

function PriorityQueue() {
  const [patientName, setPatientName] = useState("");
  const [priority, setPriority] = useState(3);

  const [queueData, setQueueData] = useState({
    queue: [],
    size: 0,
    is_empty: true,
    message: "Hospital Emergency Queue is ready",
  });

  const API_URL = "http://127.0.0.1:8000";

  const enqueuePatient = async () => {
    if (!patientName.trim()) {
      alert("Please enter patient name");
      return;
    }

    const response = await fetch(`${API_URL}/priority-queue/enqueue`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        patient_name: patientName,
        priority: Number(priority),
      }),
    });

    const data = await response.json();
    setQueueData(data);
    setPatientName("");
    setPriority(3);
  };

  const dequeuePatient = async () => {
    const response = await fetch(`${API_URL}/priority-queue/dequeue`, {
      method: "DELETE",
    });

    const data = await response.json();
    setQueueData(data);
  };

  const peekPatient = async () => {
    const response = await fetch(`${API_URL}/priority-queue/peek`);
    const data = await response.json();
    setQueueData(data);
  };

  const clearQueue = async () => {
    const response = await fetch(`${API_URL}/priority-queue/clear`, {
      method: "DELETE",
    });

    const data = await response.json();
    setQueueData(data);
  };

  const getPriorityLabel = (priority) => {
    if (priority === 1) return "Critical";
    if (priority === 2) return "Serious";
    return "Normal";
  };

  return (
    <div className="priority-page">
      <div className="priority-left-panel">
        <h2>Emergency Operations</h2>

        <input
          className="patient-input"
          type="text"
          placeholder="Enter patient name"
          value={patientName}
          onChange={(e) => setPatientName(e.target.value)}
        />

        <select
          className="priority-select"
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
        >
          <option value={1}>Priority 1 - Critical</option>
          <option value={2}>Priority 2 - Serious</option>
          <option value={3}>Priority 3 - Normal</option>
        </select>

        <button className="hospital-btn add-patient" onClick={enqueuePatient}>
          🚑 Add Patient
        </button>

        <button className="hospital-btn serve-patient" onClick={dequeuePatient}>
          🏥 Serve Patient
        </button>

        <button className="hospital-btn peek-patient" onClick={peekPatient}>
          👨‍⚕️ Check Next Patient
        </button>

        <button className="hospital-btn clear-patient" onClick={clearQueue}>
          🔄 Clear Queue
        </button>

        <div className="hospital-note">
          <h3>Hospital Rule</h3>
          <p>Patients are not served by arrival order only.</p>
          <p>Emergency patients are moved ahead based on priority.</p>
        </div>
      </div>

      <div className="priority-center-panel">
        <h2>Hospital Emergency Priority Queue</h2>

        <p className="message">{queueData.message}</p>

        <div className="hospital-stage">
          <div className="icu-room">
            <div className="icu-icon">🏥</div>
            <strong>ICU / Emergency Room</strong>
          </div>

          <div className="doctor-desk">
            <div className="doctor-icon">👨‍⚕️</div>
            <strong>Doctor / Reception</strong>
            <small>Attending highest priority patient first</small>
          </div>
        </div>

        <div className="patient-card-area">
          {queueData.queue.length === 0 ? (
            <p className="empty-text">No patients waiting</p>
          ) : (
            queueData.queue.map((patient, index) => (
              <div
                className={`patient-card priority-${patient.priority}`}
                key={index}
              >
                <small>Position {index}</small>
                <h3>{patient.name}</h3>
                <span>{getPriorityLabel(patient.priority)}</span>
                <p>Priority: {patient.priority}</p>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="priority-right-panel">
        <h2>Queue Information</h2>

        <div className="priority-info-row">
          <span>Queue Size</span>
          <strong>{queueData.size}</strong>
        </div>

        <div className="priority-info-row">
          <span>Is Empty?</span>
          <strong>{queueData.is_empty ? "Yes" : "No"}</strong>
        </div>

        <div className="priority-info-row">
          <span>Next Patient</span>
          <strong>
            {queueData.queue.length > 0 ? queueData.queue[0].name : "None"}
          </strong>
        </div>

        <div className="priority-rules">
          <h3>Priority Meaning</h3>

          <div className="rule critical-rule">
            <strong>Priority 1</strong>
            <p>Critical / Emergency</p>
          </div>

          <div className="rule serious-rule">
            <strong>Priority 2</strong>
            <p>Serious but stable</p>
          </div>

          <div className="rule normal-rule">
            <strong>Priority 3</strong>
            <p>Normal consultation</p>
          </div>
        </div>

        <div className="priority-concept-box">
          <h3>DSA Concept</h3>
          <p>
            Priority Queue removes the element with highest priority first.
            Here, lower priority number means higher urgency.
          </p>

          <code>queue.sort(key=lambda patient: patient["priority"])</code>
        </div>
      </div>
    </div>
  );
}

export default PriorityQueue;