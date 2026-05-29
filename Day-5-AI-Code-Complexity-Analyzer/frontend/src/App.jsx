
import "./App.css";
import { useState } from "react";
import axios from "axios";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#2f80ed", "#8b5cf6", "#22a06b"];

function App() {
  const [code, setCode] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const result = analysis?.analysis;
  const ml = analysis?.ml_prediction;

  const handleAnalyze = async () => {
    if (!code.trim()) {
      alert("Please paste Python code first");
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post("http://127.0.0.1:8000/analyze", {
        code,
      });
      setAnalysis(response.data);
    } catch (error) {
      console.log(error);
      alert("Backend connection failed");
    } finally {
      setLoading(false);
    }
  };

  const clearCode = () => {
    setCode("");
    setAnalysis(null);
  };

  const copyCode = async () => {
    await navigator.clipboard.writeText(code);
    alert("Code copied");
  };

  const pieData = result
    ? [
        { name: "Loops", value: result.loop_count || 0 },
        { name: "Conditions", value: result.if_count || 0 },
        { name: "Functions", value: result.function_count || 0 },
      ]
    : [
        { name: "Loops", value: 1 },
        { name: "Conditions", value: 1 },
        { name: "Functions", value: 1 },
      ];

  const score = ml?.predicted_performance_score || 0;

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="logo">AI</div>
          <div>
            <p>AI + DSA ENGINEERING</p>
            <h1>AI Code Complexity Analyzer</h1>
            <span>
              Analyze algorithm complexity, detect performance issues and get
              AI-powered optimization suggestions.
            </span>
          </div>
        </div>

        <div className="ready-box">
          <strong>READY</strong>
          <small>Paste code and click Analyze</small>
        </div>
      </header>

      <main className="dashboard">
        <section className="left-column">
          <div className="panel input-panel">
            <div className="section-title">
              <h2>Input Python Code</h2>
              <button className="small-btn danger" onClick={clearCode}>
                Clear
              </button>
            </div>

            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste your Python code here..."
            />

            <button className="analyze-btn" onClick={handleAnalyze}>
              {loading ? "Analyzing..." : "▶ Analyze Code"}
            </button>
          </div>

          <div className="panel preview-panel">
            <div className="section-title">
              <h2>Submitted Code Preview</h2>
              <button className="small-btn" onClick={copyCode}>
                Copy
              </button>
            </div>

            <pre>{code || "Code preview will appear here."}</pre>
          </div>
        </section>

        <section className="right-column">
          <div className="panel overview-panel">
            <h2>Code Analysis Overview</h2>

            <div className="metrics-grid">
              <Metric title="Total Lines" value={result?.total_lines || 0} />
              <Metric title="Loops" value={result?.loop_count || 0} />
              <Metric title="Recursion" value={result?.recursion_count || 0} />
              <Metric title="Loop Depth" value={result?.max_loop_depth || 0} />
              <Metric
                title="Time Complexity"
                value={result?.estimated_time_complexity || "-"}
              />
              <Metric
                title="Space Complexity"
                value={result?.estimated_space_complexity || "-"}
              />
            </div>
          </div>

          <div className="panel score-panel">
            <h2>ML Performance Score</h2>

            <div className="score-content">
              <div className="score-circle">{score}%</div>

              <div className="score-info">
                <div className="runtime-row">
                  <span>Predicted Runtime Heaviness</span>
                  <strong>{ml?.predicted_runtime_heaviness || "-"}</strong>
                </div>

                <div className="progress">
                  <div
                    className="progress-fill"
                    style={{ width: `${score}%` }}
                  ></div>
                </div>

                <p>
                  {score > 0
                    ? "Your code has been analyzed using static analysis and ML-based performance prediction."
                    : "Run analysis to view ML performance prediction."}
                </p>
              </div>
            </div>
          </div>

          <div className="bottom-grid">
            <div className="panel chart-panel">
              <h2>Code Distribution</h2>

              <div className="chart-layout">
                <ResponsiveContainer width="55%" height={220}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      dataKey="value"
                      innerRadius={55}
                      outerRadius={90}
                      paddingAngle={2}
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={index} fill={COLORS[index]} />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>

                <div className="legend">
                  {pieData.map((item, index) => (
                    <div key={item.name}>
                      <span style={{ background: COLORS[index] }}></span>
                      <p>{item.name}</p>
                      <strong>{result ? item.value : 0}</strong>
                    </div>
                  ))}
                </div>
              </div>

              <p className="helper-text">
                Breakdown of different code components.
              </p>
            </div>

            <div className="panel suggestions-panel">
              <h2>AI Optimization Suggestions</h2>

              {result ? (
                <div className="suggestion-list">
                  {result.optimization_suggestions.map((item, index) => (
                    <div className="suggestion" key={index}>
                      <span>{index + 1}</span>
                      <p>{item}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="empty-text">No suggestions available yet.</p>
              )}
            </div>
          </div>
        </section>
      </main>

      <footer>Built with ❤️ using React + FastAPI + ML</footer>
    </div>
  );
}

function Metric({ title, value }) {
  return (
    <div className="metric-card">
      <p>{title}</p>
      <h3>{value}</h3>
    </div>
  );
}

export default App;

