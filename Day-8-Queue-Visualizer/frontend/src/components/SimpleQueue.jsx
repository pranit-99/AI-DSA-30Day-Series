import { useState } from "react";

function SimpleQueue() {
  const [customerName, setCustomerName] = useState("");
  const [queueData, setQueueData] = useState({
    queue: [],
    front: null,
    rear: null,
    size: 0,
    message: "Queue is ready",
  });

  const API_URL = "http://127.0.0.1:8000";

  const enqueueCustomer = async () => {
    if (!customerName.trim()) {
      alert("Please enter customer name");
      return;
    }

    const response = await fetch(`${API_URL}/simple-queue/enqueue`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ customer_name: customerName }),
    });

    const data = await response.json();
    setQueueData(data);
    setCustomerName("");
  };

  const dequeueCustomer = async () => {
    const response = await fetch(`${API_URL}/simple-queue/dequeue`, {
      method: "DELETE",
    });

    const data = await response.json();
    setQueueData(data);
  };

  const peekCustomer = async () => {
    const response = await fetch(`${API_URL}/simple-queue/peek`);
    const data = await response.json();
    setQueueData(data);
  };

  const clearQueue = async () => {
    const response = await fetch(`${API_URL}/simple-queue/clear`, {
      method: "DELETE",
    });

    const data = await response.json();
    setQueueData(data);
  };

  return (
    <div className="queue-section">
      <h2>Simple Queue</h2>
      <p className="example-text">
        Real-life example: Bank Token Counter System
      </p>

      <div className="input-row">
        <input
          type="text"
          placeholder="Enter customer name"
          value={customerName}
          onChange={(e) => setCustomerName(e.target.value)}
        />

        <button onClick={enqueueCustomer}>Enqueue</button>
        <button onClick={dequeueCustomer}>Dequeue</button>
        <button onClick={peekCustomer}>Peek</button>
        <button onClick={clearQueue}>Clear</button>
      </div>

      <p className="message">{queueData.message}</p>

      <div className="stats-row">
        <div>Front: {queueData.front || "None"}</div>
        <div>Rear: {queueData.rear || "None"}</div>
        <div>Size: {queueData.size}</div>
      </div>

      <div className="queue-visual">
        {queueData.queue.length === 0 ? (
          <p className="empty-text">Queue is empty</p>
        ) : (
            queueData.queue.map((customer, index) => (
                <div className="queue-box bank-token" key={index}>
                  <small className="positive-index">Index: {index}</small>
              
                  <span className="token-number">{customer}</span>
              
                  <small className="negative-index">
                    Neg Index: {index - queueData.queue.length}
                  </small>
              
                  <div className="label-row">
                    {index === 0 && <small>Front</small>}
                    {index === queueData.queue.length - 1 && <small>Rear</small>}
                  </div>
                </div>
              ))
        )}
      </div>
      <div className="concept-panel">
  <h3>What this Simple Queue shows</h3>

  <p>
    This module represents a bank token counter system where customers are served
    in the same order they arrive.
  </p>

  <div className="concept-grid">
    <div>
      <strong>Enqueue</strong>
      <p>Adds customer at the rear using append().</p>
    </div>

    <div>
      <strong>Dequeue</strong>
      <p>Removes customer from the front using pop(0).</p>
    </div>

    <div>
      <strong>Front</strong>
      <p>First customer in the queue. In Python: queue[0]</p>
    </div>

    <div>
      <strong>Rear</strong>
      <p>Last customer in the queue. In Python: queue[-1]</p>
    </div>
  </div>
</div>
    </div>
  );
}

export default SimpleQueue;