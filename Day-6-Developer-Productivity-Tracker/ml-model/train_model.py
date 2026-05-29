import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv("sample_data.csv")

X = df[["commits", "bugs_resolved", "pull_requests", "code_reviews"]]
y = df["productive_hours"]

model = LinearRegression()
model.fit(X, y)

print("Coeficients:")
print(model.coef_)

print("\nIntercept:")
print(model.intercept_)

with open("productivity_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model Trained Successfully")