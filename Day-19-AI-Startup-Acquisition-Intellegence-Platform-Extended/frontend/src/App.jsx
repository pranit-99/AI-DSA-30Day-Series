import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    company_name: "",
    industry: "",
    founded_year: "",
    location: "",
    website: "",
    age_first_funding_year: "",
    age_last_funding_year: "",
    relationships: "",
    funding_rounds: "",
    funding_total_usd: "",
    milestones: "",
    has_VC: 0,
    has_angel: 0,
    has_roundA: 0,
    has_roundB: 0,
    has_roundC: 0,
    has_roundD: 0,
    avg_participants: "",
    is_top500: 0,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metadata, setMetadata] = useState(null);

  const API_URL = "http://127.0.0.1:8000/predict";

  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/dashboard-metadata");
        setMetadata(response.data);
      } catch (error) {
        console.error("Metadata fetch failed:", error);
      }
    };
  
    fetchMetadata();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      age_first_funding_year: Number(formData.age_first_funding_year),
      age_last_funding_year: Number(formData.age_last_funding_year),
      relationships: Number(formData.relationships),
      funding_rounds: Number(formData.funding_rounds),
      funding_total_usd: Number(formData.funding_total_usd),
      milestones: Number(formData.milestones),
      has_VC: Number(formData.has_VC),
      has_angel: Number(formData.has_angel),
      has_roundA: Number(formData.has_roundA),
      has_roundB: Number(formData.has_roundB),
      has_roundC: Number(formData.has_roundC),
      has_roundD: Number(formData.has_roundD),
      avg_participants: Number(formData.avg_participants),
      is_top500: Number(formData.is_top500),
    };

    try {
      const response = await axios.post(API_URL, payload);
      setResult(response.data);
    } catch (error) {
      console.error("Prediction failed:", error);
      alert("Backend error. Make sure FastAPI is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">🚀 StartupIntel AI</div>

        <nav>
          <div className="nav-item active">Dashboard</div>
          <div className="nav-item">Predict Startup</div>
          <div className="nav-item">Feature Importance</div>
          <div className="nav-item">Model Comparison</div>
          <div className="nav-item">History</div>
          <div className="nav-item">About</div>
        </nav>

        <div className="tip-card">
          <div className="tip-icon">💡</div>
          <h4>Investment Tip</h4>
          <p>
            Startups with strong funding history, relationships, and milestones
            usually show better acquisition potential.
          </p>
        </div>
      </aside>

      <main className="main">
        <header className="page-header">
          <div>
            <h1>
              AI Startup Acquisition Intelligence Platform{" "}
              <span>Extended</span>
            </h1>
          </div>
        </header>

        <section className="metric-grid">
          <div className="metric-card blue">
            <p>Prediction</p>
            <h3>{result ? result.prediction : "--"}</h3>
          </div>

          <div className="metric-card green">
            <p>Acquisition Probability</p>
            <h3>{result ? `${result.acquisition_probability}%` : "--"}</h3>
          </div>

          <div className="metric-card purple">
            <p>Startup Health Score</p>
            <h3>{result ? `${result.startup_health_score}/100` : "--"}</h3>
          </div>

          <div className="metric-card orange">
            <p>Risk Level</p>
            <h3>{result ? result.risk_level : "--"}</h3>
          </div>

          <div className="metric-card green">
            <p>Recommendation</p>
            <h3>{result ? result.recommendation : "--"}</h3>
          </div>
        </section>

        <section className="dashboard-grid">
          <div className="left-panel">
            <div className="panel">
              <h3>Startup Information</h3>

              <div className="startup-info-box">
                <div className="startup-logo">
                  {formData.company_name
                    ? formData.company_name.charAt(0).toUpperCase()
                    : "S"}
                </div>

                <div>
                  <h4>{formData.company_name || "Company Name"}</h4>
                  <p>
                    <b>Industry:</b> {formData.industry || "--"}
                  </p>
                  <p>
                    <b>Founded:</b> {formData.founded_year || "--"} |{" "}
                    <b>Location:</b> {formData.location || "--"}
                  </p>
                  <p>
                    <b>Website:</b> {formData.website || "--"}
                  </p>
                </div>
              </div>

              <h3>Startup Input Features</h3>

              <form onSubmit={handlePredict} className="input-form">
                <div className="form-grid">
                  <input
                    name="company_name"
                    placeholder="Company Name"
                    value={formData.company_name}
                    onChange={handleChange}
                  />

                  <input
                    name="industry"
                    placeholder="Industry"
                    value={formData.industry}
                    onChange={handleChange}
                  />

                  <input
                    name="founded_year"
                    placeholder="Founded Year"
                    value={formData.founded_year}
                    onChange={handleChange}
                  />

                  <input
                    name="location"
                    placeholder="Location"
                    value={formData.location}
                    onChange={handleChange}
                  />

                  <input
                    name="website"
                    placeholder="Website"
                    value={formData.website}
                    onChange={handleChange}
                  />

                  <input
                    name="age_first_funding_year"
                    placeholder="Age First Funding Years"
                    value={formData.age_first_funding_year}
                    onChange={handleChange}
                  />

                  <input
                    name="age_last_funding_year"
                    placeholder="Age Last Funding Years"
                    value={formData.age_last_funding_year}
                    onChange={handleChange}
                  />

                  <input
                    name="relationships"
                    placeholder="Relationships"
                    value={formData.relationships}
                    onChange={handleChange}
                  />

                  <input
                    name="funding_rounds"
                    placeholder="Funding Rounds"
                    value={formData.funding_rounds}
                    onChange={handleChange}
                  />

                  <input
                    name="funding_total_usd"
                    placeholder="Funding Total USD"
                    value={formData.funding_total_usd}
                    onChange={handleChange}
                  />

                  <input
                    name="milestones"
                    placeholder="Milestones"
                    value={formData.milestones}
                    onChange={handleChange}
                  />

                  <input
                    name="avg_participants"
                    placeholder="Average Participants"
                    value={formData.avg_participants}
                    onChange={handleChange}
                  />

                  {[
                    "has_VC",
                    "has_angel",
                    "has_roundA",
                    "has_roundB",
                    "has_roundC",
                    "has_roundD",
                    "is_top500",
                  ].map((field) => (
                    <select
                      key={field}
                      name={field}
                      value={formData[field]}
                      onChange={handleChange}
                    >
                      <option value={0}>{field}: No (0)</option>
                      <option value={1}>{field}: Yes (1)</option>
                    </select>
                  ))}
                </div>

                <button type="submit" disabled={loading}>
                  {loading ? "Predicting..." : "🚀 Predict Acquisition Probability"}
                </button>
              </form>
            </div>
          </div>

          <div className="right-panel">
            <div className="panel prediction-summary">
              <h3>Prediction Summary</h3>

              <div className="summary-content">
                <div className="circle-score">
                  {result ? `${result.acquisition_probability}%` : "--"}
                </div>

                <div>
                  <h2>{result ? result.prediction : "No Prediction Yet"}</h2>
                  <p>
                    Enter startup details and submit the form to generate
                    acquisition probability, health score, risk level, and
                    investment recommendation.
                  </p>
                </div>
              </div>

              <div className="summary-box-grid">
                <div>
                  <p>Probability</p>
                  <h4>{result ? `${result.acquisition_probability}%` : "--"}</h4>
                </div>
                <div>
                  <p>Health Score</p>
                  <h4>{result ? `${result.startup_health_score}/100` : "--"}</h4>
                </div>
                <div>
                  <p>Risk Level</p>
                  <h4>{result ? result.risk_level : "--"}</h4>
                </div>
                <div>
                  <p>Recommendation</p>
                  <h4>{result ? result.recommendation : "--"}</h4>
                </div>
              </div>
            </div>

            <div className="bottom-grid">

  <div className="panel">
    <h3>Feature Importance</h3>

    <div className="importance-list">
      {metadata?.feature_importance?.map((item) => (
        <div className="importance-row" key={item.feature}>
          <div className="importance-header">
            <span>{item.feature}</span>
            <span>{item.importance}%</span>
          </div>

          <div className="bar-bg">
            <div
              className="bar-fill"
              style={{
                width: `${item.importance}%`,
              }}
            />
          </div>
        </div>
      ))}
    </div>
  </div>

  <div className="panel model-panel">
  <h3>Model Comparison</h3>
  <p className="model-subtitle">Decision Tree vs Random Forest</p>

  <div className="model-cards">
    <div className="model-card decision">
      <p>Decision Tree</p>
      <h2>
        {metadata
          ? `${metadata.model_comparison.decision_tree_accuracy}%`
          : "--"}
      </h2>
      <div className="mini-chart">
        <span></span><span></span><span></span><span></span><span></span>
      </div>
    </div>

    <div className="model-card forest">
      <p>Random Forest</p>
      <h2>
        {metadata
          ? `${metadata.model_comparison.random_forest_accuracy}%`
          : "--"}
      </h2>
      <div className="mini-chart">
        <span></span><span></span><span></span><span></span><span></span>
      </div>
    </div>
  </div>

  <div className="improvement-card">
    <span>Improvement with Random Forest</span>
    <strong>
      {metadata
        ? `+${metadata.model_comparison.accuracy_improvement}%`
        : "--"}
    </strong>
  </div>
</div>

</div>
          </div>
        </section>

        <section className="panel recent-panel">
          <h3>Recent Prediction</h3>

          <table>
            <thead>
              <tr>
                <th>Company</th>
                <th>Industry</th>
                <th>Probability</th>
                <th>Health Score</th>
                <th>Risk Level</th>
                <th>Recommendation</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td>{formData.company_name || "--"}</td>
                <td>{formData.industry || "--"}</td>
                <td>{result ? `${result.acquisition_probability}%` : "--"}</td>
                <td>{result ? `${result.startup_health_score}/100` : "--"}</td>
                <td>{result ? result.risk_level : "--"}</td>
                <td>{result ? result.recommendation : "--"}</td>
              </tr>
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}

export default App;