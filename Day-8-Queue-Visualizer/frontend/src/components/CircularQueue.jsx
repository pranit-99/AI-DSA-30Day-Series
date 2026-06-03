import { useState } from "react";

function CircularQueue() {
  const [taskName, setTaskName] = useState("");
  const [queueData, setQueueData] = useState({
    queue: [null, null, null, null, null],
    front: -1,
    rear: -1,
    size: 0,
    capacity: 5,
    is_empty: true,
    is_full: false,
    message: "Circular Queue is ready",
  });

  const API_URL = "http://127.0.0.1:8000";

  const fetchQueue = async () => {
    const response = await fetch(`${API_URL}/circular-queue`);
    const data = await response.json();
    setQueueData(data);
  };

  const enqueueTask = async () => {
    if (!taskName.trim()) {
      alert("Please enter task name");
      return;
    }

    const response = await fetch(`${API_URL}/circular-queue/enqueue`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ task_name: taskName }),
    });

    const data = await response.json();
    setQueueData(data);
    setTaskName("");
  };

  const dequeueTask = async () => {
    const response = await fetch(`${API_URL}/circular-queue/dequeue`, {
      method: "DELETE",
    });

    const data = await response.json();
    setQueueData(data);
  };

  const peekTask = async () => {
    const response = await fetch(`${API_URL}/circular-queue/peek`);
    const data = await response.json();
    setQueueData(data);
  };

  const clearQueue = async () => {
    const response = await fetch(`${API_URL}/circular-queue/clear`, {
      method: "DELETE",
    });

    const data = await response.json();
    setQueueData(data);
  };

  const positions = [
    { top: "10%", left: "50%" },  // Index 0
    { top: "32%", left: "82%" },  // Index 1
    { top: "76%", left: "70%" },  // Index 2
    { top: "76%", left: "30%" },  // Index 3
    { top: "32%", left: "18%" },  // Index 4
  ];

  return (
    <div className="circular-page">
      <div className="circular-left-panel">
        <h2>Operations</h2>

        <button className="operation-card enqueue-card" onClick={enqueueTask}>
          ➕ Enqueue Task
          <span>Add task to CPU Queue</span>
        </button>

        <button className="operation-card dequeue-card" onClick={dequeueTask}>
          🗑 Dequeue Task
          <span>Process next task</span>
        </button>

        <button className="operation-card peek-card" onClick={peekTask}>
          👁 Peek Task
          <span>View next task</span>
        </button>

        <button className="operation-card clear-card" onClick={clearQueue}>
          🔄 Clear Queue
          <span>Reset Circular Queue</span>
        </button>

        <h3>Enqueue Input</h3>

        <input
          className="task-input"
          type="text"
          placeholder="Enter task name e.g. Task A"
          value={taskName}
          onChange={(e) => setTaskName(e.target.value)}
        />

        <button className="add-task-btn" onClick={enqueueTask}>
          Add Task
        </button>

        <div className="how-box">
          <h3>How Circular Queue Works?</h3>
          <p>✓ Fixed size queue with limited capacity</p>
          <p>✓ Uses Front and Rear pointers</p>
          <p>✓ Rear returns to index 0 using modulo</p>
          <p>✓ Efficient memory utilization</p>
        </div>
      </div>

      <div className="circular-center-panel">
        <h2>Circular Queue Visualization</h2>

        <p className="message">{queueData.message}</p>

        <div className="circle-wrapper">
          <div className="circle-ring"></div>

          <div className="cpu-center">
            <div className="computer-icon">🖥️</div>
            <strong>CPU</strong>
          </div>

          {queueData.queue.map((task, index) => (
            <div
              key={index}
              className={`circle-node 
                ${task ? "filled-node" : "empty-node"}
                ${index === queueData.front ? "front-node" : ""}
                ${index === queueData.rear ? "rear-node" : ""}
              `}
              style={positions[index]}
            >
              <small>Index {index}</small>
              <strong>{task || "Empty"}</strong>
              {index === queueData.front && <span>Front</span>}
              {index === queueData.rear && <span>Rear</span>}
            </div>
          ))}
        </div>

        <div className="formula-box">
          <strong>Useful Formula:</strong>
          <p>Rear = (Rear + 1) % Capacity</p>
          <p>Front = (Front + 1) % Capacity</p>
        </div>
      </div>

      <div className="circular-right-panel">
        <h2>Queue Information</h2>

        <div className="info-row">
          <span>Capacity</span>
          <strong>{queueData.capacity}</strong>
        </div>

        <div className="info-row">
          <span>Size</span>
          <strong>{queueData.size}</strong>
        </div>

        <div className="info-row">
          <span>Front Index</span>
          <strong>{queueData.front}</strong>
        </div>

        <div className="info-row">
          <span>Rear Index</span>
          <strong>{queueData.rear}</strong>
        </div>

        <div className="info-row">
          <span>Is Empty?</span>
          <strong>{queueData.is_empty ? "Yes" : "No"}</strong>
        </div>

        <div className="info-row">
          <span>Is Full?</span>
          <strong>{queueData.is_full ? "Yes" : "No"}</strong>
        </div>

        <div className="linear-view">
          <h3>Queue Linear View</h3>
          <div className="linear-box-row">
            {queueData.queue.map((task, index) => (
              <div key={index} className="linear-box">
                <small>{index}</small>
                <strong>{task || "-"}</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="order-box">
          <h3>Order of Processing</h3>
          <p>
            Queue processes from Front index and moves circularly using modulo.
          </p>
        </div>
      </div>
    </div>
  );
}

export default CircularQueue;