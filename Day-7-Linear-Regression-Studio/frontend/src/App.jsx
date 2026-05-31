import { useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { FaUpload, FaPlay } from "react-icons/fa";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("");
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedRegression, setSelectedRegression] = useState(
    "linear_regression"
  );

  const regressionOptions = [
    { label: "Linear Regression", value: "linear_regression" },
    { label: "Polynomial Regression", value: "polynomial_regression" },
    { label: "Ridge Regression", value: "ridge_regression" },
    { label: "Lasso Regression", value: "lasso_regression" },
  ];

  const handleTrainModel = async () => {
    if (!file) {
      setMessage("Please upload a CSV file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("regression_type", selectedRegression);

    try {
      setMessage("Training model...");

      const response = await axios.post(
        "http://127.0.0.1:8000/train",
        formData
      );

      setResult(response.data);
      setMessage("Model trained successfully.");
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Training failed."
      );
    }
  };

  const manual = result?.manual_model;
  const sklearn = result?.sklearn_model;
  const chartData = result?.chart_data || [];

  return (
    <div className="app">
      <header className="top-bar">
        <div>
          <h1>Linear Regression Studio</h1>
          <p>Manual Linear Regression vs Scikit-Learn</p>
        </div>

        <div className="action-buttons">
        <div className="custom-dropdown">
  <button
    className="dropdown-button"
    onClick={() => setIsDropdownOpen(!isDropdownOpen)}
  >
    {
      regressionOptions.find(
        (option) => option.value === selectedRegression
      )?.label
    }
    <span>⌄</span>
  </button>

  {isDropdownOpen && (
    <div className="dropdown-menu">
      {regressionOptions.map((option) => (
        <button
          key={option.value}
          className={
            selectedRegression === option.value
              ? "dropdown-item active"
              : "dropdown-item"
          }
          onClick={() => {
            setSelectedRegression(option.value);
            setIsDropdownOpen(false);
          }}
        >
          {option.label}
        </button>
      ))}
    </div>
  )}
</div>

          <label className="top-btn upload-btn">
            <FaUpload /> Upload CSV

            <input
              type="file"
              accept=".csv"
              hidden
              onChange={(e) =>
                setFile(e.target.files[0])
              }
            />
          </label>

          <button
            className="top-btn execute-btn"
            onClick={handleTrainModel}
          >
            <FaPlay /> Execute
          </button>
        </div>
      </header>

      {message && (
        <div className="message">{message}</div>
      )}

      <main className="main-layout">
        <section className="left-panel">
          <h2>Manual Linear Regression Creation</h2>

          {!manual ? (
            <div className="empty-box">
              Upload a CSV and click Execute to view
              manual calculations.
            </div>
          ) : (
            <>
              <div className="formula-grid">
                <div className="formula-card">
                  <h3>Mean of X</h3>
                  <code>x̄ = ΣX / n</code>
                  <strong>{manual.mean_x}</strong>
                </div>

                <div className="formula-card">
                  <h3>Mean of Y</h3>
                  <code>ȳ = ΣY / n</code>
                  <strong>{manual.mean_y}</strong>
                </div>

                <div className="formula-card">
                  <h3>Slope</h3>
                  <code>
                    b₁ = Σ(x-x̄)(y-ȳ) /
                    Σ(x-x̄)²
                  </code>
                  <strong>{manual.slope}</strong>
                </div>

                <div className="formula-card">
                  <h3>Intercept</h3>
                  <code>b₀ = ȳ - b₁x̄</code>
                  <strong>{manual.intercept}</strong>
                </div>

                <div className="formula-card">
                  <h3>MAE</h3>
                  <code>
                    MAE = Σ|Actual - Predicted| / n
                  </code>
                  <strong>{manual.mae}</strong>
                </div>

                <div className="formula-card">
                  <h3>MSE</h3>
                  <code>
                    MSE = Σ(Actual - Predicted)² /
                    n
                  </code>
                  <strong>{manual.mse}</strong>
                </div>

                <div className="formula-card">
                  <h3>RMSE</h3>
                  <code>RMSE = √MSE</code>
                  <strong>{manual.rmse}</strong>
                </div>

                <div className="formula-card">
                  <h3>R² Score</h3>
                  <code>R² = 1 - SSE / SST</code>
                  <strong>{manual.r2_score}</strong>
                </div>
              </div>

              <div className="equation-box">
                Regression Equation:{" "}
                {manual.equation}
              </div>

              <div className="table-box">
                <h3>Calculation Table</h3>

                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>X</th>
                        <th>Y</th>
                        <th>X - x̄</th>
                        <th>Y - ȳ</th>
                        <th>Product</th>
                        <th>(X - x̄)²</th>
                      </tr>
                    </thead>

                    <tbody>
                      {manual.calculation_table.map(
                        (row, index) => (
                          <tr key={index}>
                            <td>{row.x}</td>
                            <td>{row.y}</td>
                            <td>
                              {row.x_difference}
                            </td>
                            <td>
                              {row.y_difference}
                            </td>
                            <td>{row.product}</td>
                            <td>
                              {
                                row.x_difference_squared
                              }
                            </td>
                          </tr>
                        )
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          )}
        </section>

        <section className="right-panel">
          <div className="sklearn-panel">
            <h2>
              Scikit-Learn Linear Regression
            </h2>

            {!sklearn ? (
              <div className="empty-box">
                Scikit-Learn results will
                appear here.
              </div>
            ) : (
              <>
                <div className="sklearn-grid">
                  <div>
                    <span>Slope</span>
                    <strong>
                      {sklearn.slope}
                    </strong>
                  </div>

                  <div>
                    <span>Intercept</span>
                    <strong>
                      {sklearn.intercept}
                    </strong>
                  </div>

                  <div>
                    <span>MAE</span>
                    <strong>
                      {sklearn.mae}
                    </strong>
                  </div>

                  <div>
                    <span>MSE</span>
                    <strong>
                      {sklearn.mse}
                    </strong>
                  </div>

                  <div>
                    <span>RMSE</span>
                    <strong>
                      {sklearn.rmse}
                    </strong>
                  </div>

                  <div>
                    <span>R² Score</span>
                    <strong>
                      {sklearn.r2_score}
                    </strong>
                  </div>
                </div>

                <div className="equation-small">
                  {sklearn.equation}
                </div>
              </>
            )}
          </div>

          <div className="chart-panel">
            <h2>
              Actual vs Predicted Histogram
            </h2>

            {chartData.length === 0 ? (
              <div className="empty-box">
                Chart will appear after model
                execution.
              </div>
            ) : (
              <ResponsiveContainer
                width="100%"
                height={300}
              >
                <BarChart data={chartData}>
                  <XAxis dataKey="x" />
                  <YAxis />
                  <Tooltip />
                  <Legend />

                  <Bar dataKey="actual" name="Actual" fill="#2563eb" radius={[6, 6, 0, 0]} />

                  <Bar dataKey="predicted" name="Predicted" fill="#f97316" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;