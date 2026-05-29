from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from github_service import fetch_github_repo_activity
import pickle
import os

from productivity_logic import (
    calculate_productivity_score,
    calculate_weekly_total_commits,
    calculate_weekly_total_bugs,
    get_productivity_level,
    generate_ai_suggestion
)

app = FastAPI(title="Developer Productivity Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class GitHubRepoRequest(BaseModel):
    developer: str
    repo_url: str

model_path = os.path.join("..", "ml-model", "productivity_model.pkl")

with open(model_path, "rb") as file:
    model = pickle.load(file)


class DeveloperActivity(BaseModel):
    developer: str
    commits: int
    bugs_resolved: int
    pull_requests: int
    code_reviews: int


class WeeklyActivity(BaseModel):
    developer: str
    daily_commits: list[int]
    daily_bugs: list[int]


@app.get("/")
def home():
    return {"message": "Developer Productivity Tracker API is running"}


@app.post("/predict")
def predict_productivity(activity: DeveloperActivity):
    input_data = [[
        activity.commits,
        activity.bugs_resolved,
        activity.pull_requests,
        activity.code_reviews
    ]]

    predicted_hours = model.predict(input_data)[0]

    productivity_score = calculate_productivity_score(
        activity.commits,
        activity.bugs_resolved,
        activity.pull_requests,
        activity.code_reviews
    )
    productivity_level = get_productivity_level(productivity_score)
    ai_suggestion = generate_ai_suggestion(
    productivity_score,
    predicted_hours
)

    return {
        "developer": activity.developer,
        "predicted_productive_hours": round(predicted_hours, 2),
        "productivity_score": productivity_score,
        "productivity_level": productivity_level,
        "ai_suggestion": ai_suggestion
    }


@app.post("/weekly-summary")
def weekly_summary(activity: WeeklyActivity):
    total_commits = calculate_weekly_total_commits(activity.daily_commits)
    total_bugs = calculate_weekly_total_bugs(activity.daily_bugs)

    return {
        "developer": activity.developer,
        "total_weekly_commits": total_commits,
        "total_weekly_bugs_resolved": total_bugs
    }

@app.post("/github-analyze")
def github_analyze(request: GitHubRepoRequest):
    activity = fetch_github_repo_activity(request.repo_url)

    input_data = [[
        activity["commits"],
        activity["bugs_resolved"],
        activity["pull_requests"],
        activity["code_reviews"]
    ]]

    predicted_hours = model.predict(input_data)[0]

    productivity_score = calculate_productivity_score(
        activity["commits"],
        activity["bugs_resolved"],
        activity["pull_requests"],
        activity["code_reviews"]
    )

    productivity_level = get_productivity_level(productivity_score)

    ai_suggestion = generate_ai_suggestion(
        productivity_score,
        predicted_hours
    )

    return {
        "developer": request.developer,
        "repo_url": request.repo_url,
        "commits": activity["commits"],
        "bugs_resolved": activity["bugs_resolved"],
        "pull_requests": activity["pull_requests"],
        "code_reviews": activity["code_reviews"],
        "predicted_productive_hours": round(predicted_hours, 2),
        "productivity_score": productivity_score,
        "productivity_level": productivity_level,
        "ai_suggestion": ai_suggestion
    }