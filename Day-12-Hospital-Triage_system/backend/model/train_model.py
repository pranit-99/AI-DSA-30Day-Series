import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

#Here we will load dataset
data = pd.read_csv("patient_data.csv")

#Features
X = data[
    [
        "age",
        "heart_rate",
        "blood_pressure",
        "oxygen_level",
        "temperature"
    ]
]

#Target
y = data["critical"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LogisticRegression()

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(
    model,
    "patient_triage_model.pkl"
)

print("Model Saved Successfully")

print("Coefficients:")
for feature, coef in zip(X.columns, model.coef_[0]):
    print(feature, ":", coef)

print("Intercept:", model.intercept_[0])