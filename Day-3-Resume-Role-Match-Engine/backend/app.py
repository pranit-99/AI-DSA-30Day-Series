from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from resume_role_match import analyze_resume_match

app = FastAPI(title="Resume to Role Match Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str


@app.get("/")
def home():
    return {
        "message": "Resume to Role Match Engine API is running"
    }


@app.post("/match")
def match_resume_to_role(request: MatchRequest):
    if not request.resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty"
        )
    
    if not request.jd_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description text cannot be empty."
        )
    result = analyze_resume_match(
        request.resume_text,
        request.jd_text
    )

    return result