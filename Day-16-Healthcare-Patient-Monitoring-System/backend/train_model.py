import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


df = pd.read_csv("data/patient_vitals.csv")

features = [
    "age",
    "spo2",
    "respiratory_rate",
    "systolic_bp",
    "diastolic_bp",
    "temperature",
    "overall_risk",
    "comorbidity_count"
]

target = "heart_rate"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = SVR(kernel="rbf", C=100, gamma="scale", epsilon=0.1)

model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("SVR Model Training Completed")
print("Mean Absolute Error:", mae)
print("Mean Squared Error:", mse)
print("R2 Score:", r2)

joblib.dump(model, "models/heart_rate_svr_model.pkl")
joblib.dump(scaler, "models/heart_rate_scaler.pkl")

print("Model saved successfully")