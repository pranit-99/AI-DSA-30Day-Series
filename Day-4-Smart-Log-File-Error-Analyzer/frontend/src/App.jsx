import { useMemo, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  AreaChart,
  Area,
  XAxis,
} from "recharts";

import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [searchTerm, setSearchTerm] = useState("");
  const [severityFilter, setSeverityFilter] = useState("ALL");

  const getAIInsight = () => {
    if (!analysisResult || analysisResult.top_errors.length === 0) {
      return "Upload logs to generate AI-driven insights.";
    }
  
    const topError = analysisResult.top_errors[0];
  
    const highPercentage =
      chartData.find((item) => item.name === "HIGH")?.percentage || 0;
  
    if (Number(highPercentage) >= 50) {
      return `High severity errors contribute ${highPercentage}% of detected failures. ${topError.error} is the most frequent issue and should be investigated immediately.`;
    }
  
    if (Number(highPercentage) >= 25) {
      return `High severity errors contribute ${highPercentage}% of detected failures. ${topError.error} is the top recurring issue and should be prioritized.`;
    }
  
    return `System risk is currently moderate. ${topError.error} is the most frequent issue, but high severity impact is limited to ${highPercentage}%.`;
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert("Please select a log file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);

      const response = await fetch("http://127.0.0.1:8000/upload-log", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      setAnalysisResult(data);
    } catch (error) {
      console.error(error);
      alert("Failed to analyze logs.");
    } finally {
      setLoading(false);
    }
  };

  const getSeverityClass = (severity) => {
    if (severity === "HIGH") return "severity high";
    if (severity === "MEDIUM") return "severity medium";
    return "severity low";
  };

  const getSeverityCounts = () => {
    if (!analysisResult) {
      return {
        HIGH: 0,
        MEDIUM: 0,
        LOW: 0,
      };
    }

    const counts = {
      HIGH: 0,
      MEDIUM: 0,
      LOW: 0,
    };

    analysisResult.top_errors.forEach((item) => {
      counts[item.severity] += item.count;
    });

    return counts;
  };

  const severityCounts = getSeverityCounts();

  const totalSeverityImpact =
  severityCounts.HIGH + severityCounts.MEDIUM + severityCounts.LOW;

const chartData = [
  {
    name: "HIGH",
    value: severityCounts.HIGH,
    percentage: totalSeverityImpact
      ? ((severityCounts.HIGH / totalSeverityImpact) * 100).toFixed(1)
      : 0,
  },
  {
    name: "MEDIUM",
    value: severityCounts.MEDIUM,
    percentage: totalSeverityImpact
      ? ((severityCounts.MEDIUM / totalSeverityImpact) * 100).toFixed(1)
      : 0,
  },
  {
    name: "LOW",
    value: severityCounts.LOW,
    percentage: totalSeverityImpact
      ? ((severityCounts.LOW / totalSeverityImpact) * 100).toFixed(1)
      : 0,
  },
];

  const COLORS = ["#ef4444", "#f59e0b", "#22c55e"];

  const filteredErrors = useMemo(() => {
    if (!analysisResult) return [];

    return analysisResult.top_errors.filter((item) => {
      const matchesSearch = item.error
        .toLowerCase()
        .includes(searchTerm.toLowerCase());

      const matchesSeverity =
        severityFilter === "ALL" ||
        item.severity === severityFilter;

      return matchesSearch && matchesSeverity;
    });
  }, [analysisResult, searchTerm, severityFilter]);

  const trendData = [
    { time: "09 AM", errors: 2 },
    { time: "10 AM", errors: 4 },
    { time: "11 AM", errors: 6 },
    { time: "12 PM", errors: 3 },
    { time: "01 PM", errors: 8 },
    { time: "02 PM", errors: 5 },
  ];

  return (
    <div className="app">
      <div className="dashboard-layout">

        {/* LEFT PANEL */}
        <div className="left-panel">

          <div className="hero-card">
            <p className="eyebrow">AI + DSA Observability</p>

            <h1>Smart Log Analyzer</h1>

            <p className="subtitle">
              Analyze logs using HashMap frequency counting and Machine Learning severity prediction.
            </p>

            <div className="upload-section">
              <input
                type="file"
                accept=".log,.txt"
                onChange={handleFileChange}
              />

              <button onClick={handleAnalyze}>
                {loading ? "Analyzing Logs..." : "Analyze Logs"}
              </button>
            </div>

            {loading && (
              <div className="loading-box">
                <p>Scanning logs...</p>
                <p>Running ML severity prediction...</p>
                <p>Detecting critical failures...</p>
              </div>
            )}
          </div>

          <div className="summary-grid">

            <div className="summary-card">
              <p>Total Logs</p>
              <h2>{analysisResult?.total_logs || 0}</h2>
            </div>

            <div className="summary-card">
              <p>Total Errors</p>
              <h2>{analysisResult?.total_errors || 0}</h2>
            </div>

            <div className="summary-card high-card">
              <p>High Risk</p>
              <h2>{severityCounts.HIGH}</h2>
            </div>

            <div className="summary-card medium-card">
              <p>Medium Risk</p>
              <h2>{severityCounts.MEDIUM}</h2>
            </div>

            <div className="summary-card low-card">
              <p>Low Risk</p>
              <h2>{severityCounts.LOW}</h2>
            </div>

          </div>

          <div className="insight-card">
            <h3>AI Insights</h3>
              <p>{getAIInsight()}</p>
          </div>

        </div>

        {/* CENTER PANEL */}
        <div className="center-panel">

          <div className="toolbar">

            <input
              type="text"
              placeholder="Search errors..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />

            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
            >
              <option value="ALL">All Severity</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>

          </div>

          <div className="error-list">

            {filteredErrors.length === 0 && (
              <div className="empty-card">
                Upload and analyze logs to display insights.
              </div>
            )}

            {filteredErrors.map((item, index) => (
              <div className="error-card" key={index}>

                <div className="error-top">
                  <h3>{item.error}</h3>

                  <div className={getSeverityClass(item.severity)}>
                    {item.severity}
                  </div>
                </div>

                <div className="error-meta">
                  <span>{item.category}</span>
                  <span>Count: {item.count}</span>
                </div>

                <div className="severity-track">
                  <div
                    className={`severity-fill ${item.severity.toLowerCase()}`}
                  ></div>
                </div>

              </div>
            ))}

          </div>

        </div>

        {/* RIGHT PANEL */}
        <div className="right-panel">

          <div className="chart-card">
            <h3>Severity Distribution</h3>

            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={chartData}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={65}
                  outerRadius={95}
                  paddingAngle={4}
                >
                  {chartData.map((entry, index) => (
                    <Cell
                      key={index}
                      fill={COLORS[index]}
                    />
                  ))}
                </Pie>

                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="chart-legend">

  {chartData.map((item, index) => (
    <div className="legend-item" key={index}>

      <div className="legend-left">
        <div
          className="legend-color"
          style={{ background: COLORS[index] }}
        ></div>

        <span>{item.name}</span>
      </div>

      <div className="legend-right">
        {item.percentage}%
      </div>

    </div>
  ))}

</div>
          </div>

          <div className="timeline-card">
            <h3>Error Trend</h3>

            <ResponsiveContainer width="100%" height={180}>
              <AreaChart data={trendData}>
                <XAxis dataKey="time" />
                <Tooltip />

                <Area
                  type="monotone"
                  dataKey="errors"
                  stroke="#06b6d4"
                  fill="#0891b2"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

        </div>

      </div>
    </div>
  );
}

export default App;