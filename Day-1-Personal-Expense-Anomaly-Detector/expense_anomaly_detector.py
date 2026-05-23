from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import math
import csv
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def analyze_expense_data(expenses):
    total_spending = sum(expenses)
    number_of_days = len(expenses)
    average_spending = total_spending / number_of_days

    sum_of_squared_differences = 0

    for expense in expenses:
        difference = expense - average_spending
        squared_difference = difference ** 2
        sum_of_squared_differences += squared_difference

    variance = sum_of_squared_differences / number_of_days
    standard_deviation = math.sqrt(variance)

    anomaly_count = 0
    analysis = []

    for day, expense in enumerate(expenses, start=1):
        z_score = 0 if standard_deviation == 0 else (expense - average_spending) / standard_deviation

        if average_spending == 0:
            percentage_difference = 0
        else:
            percentage_difference = ((expense - average_spending) / average_spending) * 100

        if abs(z_score) < 2:
            severity = "NORMAL"
        elif abs(z_score) < 3:
            severity = "MODERATE ANOMALY"
            anomaly_count += 1
        else:
            severity = "SEVERE ANOMALY"
            anomaly_count += 1

        analysis.append({
            "day": day,
            "expense": round(expense, 2),
            "zScore": round(z_score, 2),
            "percentageDifference": round(percentage_difference, 2),
            "severity": severity
        })

    anomaly_percentage = (anomaly_count / number_of_days) * 100

    if anomaly_count == 0:
        risk_level = "LOW RISK"
    elif anomaly_count <= 2:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "HIGH RISK"

    return {
        "summary": {
            "totalExpenses": number_of_days,
            "totalSpending": round(total_spending, 2),
            "averageSpending": round(average_spending, 2),
            "variance": round(variance, 2),
            "standardDeviation": round(standard_deviation, 2),
            "anomaliesFound": anomaly_count,
            "anomalyPercentage": round(anomaly_percentage, 2),
            "riskLevel": risk_level
        },
        "analysis": analysis
    }


@app.get("/analyze-expenses")
def analyze_expenses():
    expenses = []

    try:
        with open("expenses.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                expenses.append(float(row["expense"]))

        if len(expenses) < 2:
            return {"error": "CSV must contain at least 2 expenses."}

    except FileNotFoundError:
        return {"error": "expenses.csv file not found."}

    except KeyError:
        return {"error": "CSV must contain an 'expense' column."}

    except ValueError:
        return {"error": "Invalid expense value in CSV. Please use numbers only."}

    return analyze_expense_data(expenses)


@app.post("/upload-expenses")
async def upload_expenses(file: UploadFile = File(...)):
    contents = await file.read()
    decoded_file = contents.decode("utf-8")

    reader = csv.DictReader(io.StringIO(decoded_file))
    expenses = []

    try:
        for row in reader:
            expenses.append(float(row["expense"]))

        if len(expenses) < 2:
            return {"error": "CSV must contain at least 2 expenses."}

    except KeyError:
        return {"error": "CSV must contain an 'expense' column."}

    except ValueError:
        return {"error": "Invalid expense value in CSV. Please use numbers only."}

    return analyze_expense_data(expenses)