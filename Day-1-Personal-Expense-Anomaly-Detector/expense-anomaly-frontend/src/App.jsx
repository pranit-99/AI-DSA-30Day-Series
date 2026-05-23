import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import axios from "axios";
import "./App.css";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/analyze-expenses")
      .then((response) => setData(response.data))
      .catch((error) => console.error("Error fetching expense data:", error));
  }, []);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload-expenses",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setData(response.data);
    } catch (error) {
      console.error("Upload failed:", error);
    }
  };

  return (
    <div className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">AI Finance Analytics</p>
          <h1>Personal Expense Anomaly Detector</h1>
          <p>
            Upload spending data and detect unusual expense behavior using
            statistical anomaly detection.
          </p>
        </div>

        <div className="upload-section">
          <input type="file" accept=".csv" onChange={handleFileUpload} />
        </div>
      </header>

      {data ? (
        <>
          <div className="summary-grid">
            <div className="card">
              <h3>Total Spending</h3>
              <p>${data.summary.totalSpending}</p>
            </div>

            <div className="card">
              <h3>Average Spending</h3>
              <p>${data.summary.averageSpending}</p>
            </div>

            <div className="card">
              <h3>Anomalies Found</h3>
              <p>{data.summary.anomaliesFound}</p>
            </div>

            <div className="card">
              <h3>Risk Level</h3>
              <p>
                <span
                  className={`risk-badge ${data.summary.riskLevel
                    .toLowerCase()
                    .replaceAll(" ", "-")}`}
                >
                  {data.summary.riskLevel}
                </span>
              </p>
            </div>
          </div>

          <div className="dashboard-row">
            <div className="chart-section">
              <h2>Expense Trend</h2>

              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data.analysis}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="expense"
                    stroke="#2563eb"
                    strokeWidth={3}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="table-section">
              <h2>Analysis Table</h2>

              <table>
                <thead>
                  <tr>
                    <th>Day</th>
                    <th>Expense</th>
                    <th>Status</th>
                  </tr>
                </thead>

                <tbody>
                  {data.analysis.map((item) => (
                    <tr key={item.day}>
                      <td>{item.day}</td>
                      <td>${item.expense}</td>
                      <td>
                        <span
                          className={`status-badge ${item.severity
                            .toLowerCase()
                            .replaceAll(" ", "-")}`}
                        >
                          {item.severity}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      ) : (
        <p className="loading">Loading expense analysis...</p>
      )}
    </div>
  );
}

export default App;