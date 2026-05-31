import os
import shutil
import numpy as np

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from linear_regression_oop import LinearRegressionBuilding, load_data_from_csv


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trained_model = None


class PredictionRequest(BaseModel):
    hours: float


@app.get("/")
def home():
    return {"message": "Linear Regression API is running"}


@app.post("/train")
def train_model(file: UploadFile = File(...), regression_type: str = Form(...)):
    global trained_model

    regression_type = regression_type.strip().lower()
    implemented_models = ["linear_regression"]
    if regression_type not in implemented_models:
        raise HTTPException(
            status_code=400,
            detail=f"{regression_type} is not implemented yet"
        )

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        x_values, y_values = load_data_from_csv(file_path)

        # Manual model
        trained_model = LinearRegressionBuilding(x_values, y_values)
        trained_model.train()
        trained_model.evaluate()

        manual_results = trained_model.get_manual_results()
        chart_data = trained_model.get_chart_data()

        # Scikit-Learn model
        X = np.array(x_values).reshape(-1, 1)
        Y = np.array(y_values)

        sklearn_model = LinearRegression()
        sklearn_model.fit(X, Y)

        sklearn_predictions = sklearn_model.predict(X)

        sklearn_mae = mean_absolute_error(Y, sklearn_predictions)
        sklearn_mse = mean_squared_error(Y, sklearn_predictions)
        sklearn_rmse = np.sqrt(sklearn_mse)
        sklearn_r2 = r2_score(Y, sklearn_predictions)

        sklearn_results = {
            "slope": round(sklearn_model.coef_[0], 2),
            "intercept": round(sklearn_model.intercept_, 2),
            "equation": f"y = {round(sklearn_model.intercept_, 2)} + {round(sklearn_model.coef_[0], 2)}x",
            "mae": round(sklearn_mae, 2),
            "mse": round(sklearn_mse, 2),
            "rmse": round(sklearn_rmse, 2),
            "r2_score": round(sklearn_r2, 2)
        }

        return {
            "message": "Model trained successfully",
            "manual_model": manual_results,
            "sklearn_model": sklearn_results,
            "chart_data": chart_data,
            "data_points": len(x_values)
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/predict")
def predict_marks(request: PredictionRequest):
    if trained_model is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload CSV and train the model first"
        )

    predicted_marks = trained_model.predict(request.hours)

    return {
        "hours": request.hours,
        "predicted_marks": round(predicted_marks, 2),
        "equation": f"y = {round(trained_model.intercept, 2)} + {round(trained_model.slope, 2)}x"
    }