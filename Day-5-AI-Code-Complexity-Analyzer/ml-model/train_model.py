import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib


data = pd.read_csv("code_complexity_dataset.csv")

X = data[
    [
        "total_lines",
        "loop_count",
        "if_count",
        "function_count",
        "recursion_count",
        "max_loop_depth",
    ]
]

y = data["performance_score"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Model trained successfully")
print("Model saved as model.pkl")