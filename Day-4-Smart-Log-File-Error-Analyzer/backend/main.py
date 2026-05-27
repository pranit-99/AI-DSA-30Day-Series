import shutil
from fastapi import FastAPI, UploadFile, File
from log_analyzer import analyze_logs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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


@app.get("/")
def home():
    return {"message": "Smart Log File Error Analyzer Backend is running"}


@app.get("/analyze-sample-log")
def analyze_sample_log():
    file_path = "../sample_logs/app.log"
    result = analyze_logs(file_path)
    return result


@app.post("/upload-log")
def upload_log(file: UploadFile = File(...)):
    temp_file_path = f"uploaded_{file.filename}"

    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_logs(temp_file_path)

    return result