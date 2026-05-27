import { useState } from "react";
import mammoth from "mammoth";
import * as pdfjsLib from "pdfjs-dist";
import pdfWorker from "pdfjs-dist/build/pdf.worker.min.mjs?url";
import "./App.css";

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorker;

function App() {
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [fileName, setFileName] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const extractPdfText = async (file) => {
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;

    let text = "";

    for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
      const page = await pdf.getPage(pageNumber);
      const content = await page.getTextContent();
      text += content.items.map((item) => item.str).join(" ") + "\n";
    }

    return text;
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setError("");
    setFileName(file.name);

    try {
      const fileExtension = file.name.split(".").pop().toLowerCase();

      if (fileExtension === "txt") {
        const text = await file.text();
        setResumeText(text);
      } else if (fileExtension === "pdf") {
        const text = await extractPdfText(file);
        setResumeText(text);
      } else if (fileExtension === "docx") {
        const arrayBuffer = await file.arrayBuffer();
        const result = await mammoth.extractRawText({ arrayBuffer });
        setResumeText(result.value);
      } else {
        setError("Unsupported file type. Please upload .txt, .pdf, or .docx file.");
      }
    } catch (err) {
      setError("Could not read this file. Please try another resume file.");
    }
  };

  const handleAnalyze = async () => {
    setError("");
    setResult(null);

    if (!resumeText.trim()) {
      setError("Please add resume text or upload a resume file.");
      return;
    }

    if (!jdText.trim()) {
      setError("Please paste the job description.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/match", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          resume_text: resumeText,
          jd_text: jdText
        })
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Something went wrong.");
        return;
      }

      setResult(data);
    } catch (err) {
      setError("Backend is not running or API connection failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResumeText("");
    setJdText("");
    setFileName("");
    setResult(null);
    setError("");
  };

  return (
    <div className="app-container">
      <div className="hero-section">
        <h1>Resume to Role Match Engine</h1>
        <p>Analyze resume keywords against a job description using NLP and DSA concepts.</p>
      </div>

      <div className="main-card">
        <div className="input-section">
          <div className="input-box">
            <h2>Resume</h2>

            <label className="file-upload">
              Upload Resume File
              <input
                type="file"
                accept=".txt,.pdf,.docx"
                onChange={handleFileUpload}
              />
            </label>

            {fileName && <p className="file-name">Selected: {fileName}</p>}

            <textarea
              placeholder="Paste your resume text here or upload .txt, .pdf, or .docx file..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
            />
          </div>

          <div className="input-box">
            <h2>Job Description</h2>

            <textarea
              className="jd-textarea"
              placeholder="Paste job description here..."
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
            />
          </div>
        </div>

        <div className="button-group">
          <button className="analyze-btn" onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Match"}
          </button>

          <button className="reset-btn" onClick={handleReset}>
            Reset
          </button>
        </div>

        {error && <p className="error-message">{error}</p>}

        {result && (
          <div className="results-section">
            <h2>Analysis Results</h2>

            <div className="score-grid">
              <div className="score-card">
                <h3>Basic Score</h3>
                <p>{result.basic_match_score}%</p>
              </div>

              <div className="score-card">
                <h3>Weighted Score</h3>
                <p>{result.weighted_match_score}%</p>
              </div>
            </div>

            <div className="keyword-section">
              <div className="keyword-box">
                <h3>Matched Keywords</h3>
                <div className="keyword-list">
                  {result.matched_keywords.map((keyword, index) => (
                    <span className="matched-keyword" key={index}>
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>

              <div className="keyword-box">
                <h3>Top Missing Keywords</h3>
                <div className="keyword-list">
                  {result.top_missing_keywords.map((keyword, index) => (
                    <span className="missing-keyword" key={index}>
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="suggestion-box">
              <h3>Suggestion</h3>
              <p>{result.suggestion}</p>
            </div>
          </div>
        )}
      </div>

      <footer className="footer">
        <p>Day 3 Project · DSA: Strings, HashMap, Set · AI/ML: NLP Keyword Extraction</p>
      </footer>
    </div>
  );
}

export default App;