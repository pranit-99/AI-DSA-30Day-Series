import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier


# Load Dataset
df = pd.read_csv("sample_data.csv")

# Features
X = df[[
    "volatility",
    "avg_return"
]]

# Labels
y = df["risk"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Model
model = XGBClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.1,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(
    y_test,
    predictions
)

print("Accuracy:", accuracy)

# Save Model
joblib.dump(
    model,
    "portfolio_risk_model.pkl"
)

print("Model Saved Successfully")