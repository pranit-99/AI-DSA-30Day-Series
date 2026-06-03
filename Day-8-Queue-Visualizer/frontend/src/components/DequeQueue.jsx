import { useState } from "react";

function DequeQueue() {
  const [pageName, setPageName] = useState("");

  const [queueData, setQueueData] = useState({
    queue: [],
    front: null,
    rear: null,
    size: 0,
    is_empty: true,
    message: "Browser History Deque is ready",
  });

  const API_URL = "http://127.0.0.1:8000";

  const sendPageRequest = async (endpoint) => {
    if (!pageName.trim()) {
      alert("Please enter page name");
      return;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ page_name: pageName }),
    });

    const data = await response.json();
    setQueueData(data);
    setPageName("");
  };

  const sendDeleteRequest = async (endpoint) => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: "DELETE",
    });

    const data = await response.json();
    setQueueData(data);
  };

  const sendGetRequest = async (endpoint) => {
    const response = await fetch(`${API_URL}${endpoint}`);
    const data = await response.json();
    setQueueData(data);
  };

  return (
    <div className="deque-page">
      <div className="deque-left-panel">
        <h2>Browser Operations</h2>

        <input
          className="page-input"
          type="text"
          placeholder="Enter page name e.g. Google"
          value={pageName}
          onChange={(e) => setPageName(e.target.value)}
        />

        <button
          className="deque-btn add-front-btn"
          onClick={() => sendPageRequest("/deque/add-front")}
        >
          ⬅ Add Front
        </button>

        <button
          className="deque-btn add-rear-btn"
          onClick={() => sendPageRequest("/deque/add-rear")}
        >
          Add Rear ➡
        </button>

        <button
          className="deque-btn remove-front-btn"
          onClick={() => sendDeleteRequest("/deque/remove-front")}
        >
          ⬅ Remove Front
        </button>

        <button
          className="deque-btn remove-rear-btn"
          onClick={() => sendDeleteRequest("/deque/remove-rear")}
        >
          Remove Rear ➡
        </button>

        <button
          className="deque-btn peek-front-btn"
          onClick={() => sendGetRequest("/deque/peek-front")}
        >
          👁 Peek Front
        </button>

        <button
          className="deque-btn peek-rear-btn"
          onClick={() => sendGetRequest("/deque/peek-rear")}
        >
          👁 Peek Rear
        </button>

        <button
          className="deque-btn clear-deque-btn"
          onClick={() => sendDeleteRequest("/deque/clear")}
        >
          🔄 Clear
        </button>
      </div>

      <div className="deque-center-panel">
        <h2>Double Ended Queue Visualizer</h2>
        <p className="message">{queueData.message}</p>

        <div className="browser-frame">
          <div className="browser-top-bar">
            <span></span>
            <span></span>
            <span></span>
            <div className="browser-url">Browser History / Undo-Redo</div>
          </div>

          <div className="deque-visual-area">
            <div className="side-label left-side-label">Front</div>

            <div className="deque-track">
              {queueData.queue.length === 0 ? (
                <p className="empty-text">No pages in history</p>
              ) : (
                queueData.queue.map((page, index) => (
                  <div className="web-page-card" key={index}>
                    <small>Index {index}</small>
                    <div className="page-icon">🌐</div>
                    <strong>{page}</strong>
                    <small>
                      Neg Index: {index - queueData.queue.length}
                    </small>

                    <div className="deque-badges">
                      {index === 0 && <span>Front</span>}
                      {index === queueData.queue.length - 1 && <span>Rear</span>}
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="side-label right-side-label">Rear</div>
          </div>
        </div>

        <div className="deque-concept-row">
          <div>
            <strong>insert(0, value)</strong>
            <p>Adds page at front</p>
          </div>
          <div>
            <strong>append(value)</strong>
            <p>Adds page at rear</p>
          </div>
          <div>
            <strong>pop(0)</strong>
            <p>Removes page from front</p>
          </div>
          <div>
            <strong>pop()</strong>
            <p>Removes page from rear</p>
          </div>
        </div>
      </div>

      <div className="deque-right-panel">
        <h2>Deque Information</h2>

        <div className="deque-info-row">
          <span>Front Page</span>
          <strong>{queueData.front || "None"}</strong>
        </div>

        <div className="deque-info-row">
          <span>Rear Page</span>
          <strong>{queueData.rear || "None"}</strong>
        </div>

        <div className="deque-info-row">
          <span>Size</span>
          <strong>{queueData.size}</strong>
        </div>

        <div className="deque-info-row">
          <span>Is Empty?</span>
          <strong>{queueData.is_empty ? "Yes" : "No"}</strong>
        </div>

        <div className="deque-rule-box">
          <h3>What is Deque?</h3>
          <p>
            A Double Ended Queue allows insertion and deletion from both front
            and rear ends.
          </p>
        </div>

        <div className="deque-rule-box">
          <h3>Real-life Example</h3>
          <p>
            Browser history and undo-redo systems can move from both directions,
            making Deque a strong fit.
          </p>
        </div>
      </div>
    </div>
  );
}

export default DequeQueue;