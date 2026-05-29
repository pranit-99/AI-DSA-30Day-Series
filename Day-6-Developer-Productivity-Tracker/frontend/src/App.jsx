import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    developer: "Pranit Mhatre",
    repo_url: "https://github.com/facebook/react",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const avatarUrl =
    "https://api.dicebear.com/7.x/adventurer/svg?seed=developer";

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const analyzeGitHubRepo = async () => {
    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/github-analyze",
        formData
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Backend API is not running or GitHub repo URL is invalid.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="dashboard">
        <aside className="profile-panel">
          <div className="avatar-card">
            <img src={avatarUrl} alt="Developer Avatar" className="avatar" />
            <h1>Developer Productivity Tracker</h1>
            <p>
              Analyze GitHub repository activity and predict developer
              productivity using FastAPI, GitHub API, DSA logic, and ML.
            </p>
          </div>

          <div className="input-card">
            <label>Developer Name</label>
            <input
              name="developer"
              value={formData.developer}
              onChange={handleChange}
              placeholder="Enter developer name"
            />

            <label>GitHub Repository Link</label>
            <input
              name="repo_url"
              value={formData.repo_url}
              onChange={handleChange}
              placeholder="https://github.com/owner/repo"
            />

            <button onClick={analyzeGitHubRepo} disabled={loading}>
              {loading ? "Analyzing Repository..." : "Analyze GitHub Repo"}
            </button>
          </div>
        </aside>

        <main className="analytics-panel">
          <div className="hero-card">
            <div>
              <span className="tag">AI + DSA + GitHub API</span>
              <h2>Repository Productivity Insights</h2>
              <p>
                Enter a GitHub repository URL to fetch commits, pull requests,
                closed issues, and generate ML-based productivity prediction.
              </p>
            </div>

            <div className="level-box">
              <span>Level</span>
              <strong>{result ? result.productivity_level : "--"}</strong>
            </div>
          </div>

          <div className="metrics-grid">
            <div className="metric-card">
              <span>Commits</span>
              <h3>{result ? result.commits : "--"}</h3>
              <p>GitHub Activity</p>
            </div>

            <div className="metric-card">
              <span>Pull Requests</span>
              <h3>{result ? result.pull_requests : "--"}</h3>
              <p>Collaboration Signal</p>
            </div>

            <div className="metric-card">
              <span>Bugs Resolved</span>
              <h3>{result ? result.bugs_resolved : "--"}</h3>
              <p>Closed Issues</p>
            </div>

            <div className="metric-card">
              <span>Code Reviews</span>
              <h3>{result ? result.code_reviews : "--"}</h3>
              <p>Review Activity</p>
            </div>
          </div>

          <div className="result-row">
            <div className="score-card">
              <h2>Productivity Score</h2>
              <div className="score-circle">
                {result ? result.productivity_score : "--"}
              </div>
              <p>Calculated using weighted DSA logic.</p>
            </div>

            <div className="prediction-card">
              <h2>Predicted Productive Hours</h2>
              <h1>{result ? result.predicted_productive_hours : "--"}</h1>
              <p>Linear Regression ML output.</p>
            </div>
          </div>

          <div className="suggestion-card">
            <h2>AI Suggestion</h2>
            <p>
              {result
                ? result.ai_suggestion
                : "Submit a GitHub repository link to generate personalized productivity suggestions."}
            </p>
          </div>

          <div className="concept-card">
            <h2>Concepts Covered</h2>
            <div className="concept-list">
              <span>Arrays</span>
              <span>Prefix Sum</span>
              <span>Linear Regression</span>
              <span>FastAPI</span>
              <span>React</span>
              <span>GitHub API</span>
              <span>Scikit-Learn</span>
              <span>REST API</span>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;