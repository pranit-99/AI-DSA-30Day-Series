import { useState } from "react";
import "./App.css"

import SimpleQueue from "./components/SimpleQueue";
import CircularQueue from "./components/CircularQueue";
import PriorityQueue from "./components/PriorityQueue";
import DequeQueue from "./components/DequeQueue";

function App() {
  const [selectedQueue, setSelectedQueue] = useState("");
  return (
    <div className="app-container">
      <h1>Queue Visualizer</h1>
      <p className="subtitle">
        Learn Queue Data Structures using Python backend and React visualization
      </p>

      <div className="queue-tabs">
        <button onClick={() => setSelectedQueue("simple")}>
          Simple Queue
        </button>

        <button onClick={() => setSelectedQueue("circular")}>
          Circular Queue
        </button>

        <button onClick={() => setSelectedQueue("priority")}>
          Priority Queue
        </button>

        <button onClick={() => setSelectedQueue("deque")}>
          Double Ended Queue
        </button>
      </div>

      {selectedQueue === "" && (
      <div className="welcome-panel">
      <h2>Select a Queue Type</h2>
      <p>
      Choose any queue from above to visualize how Python DSA logic works behind the screen.
      </p>
      </div>
      )}

    {selectedQueue === "simple" && <SimpleQueue />}
    {selectedQueue === "circular" && <CircularQueue />}
    {selectedQueue === "priority" && <PriorityQueue />}
    {selectedQueue === "deque" && <DequeQueue />}
    </div>
  );
}
export default App;