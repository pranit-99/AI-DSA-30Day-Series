from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import joblib

#Load DataSet
df = pd.read_csv("data/startup_data.csv")

print("DataSet Loaded Successfully")
print("Shape:", df.shape)

# Select useful input features
features = [
    "age_first_funding_year",
    "age_last_funding_year",
    "relationships",
    "funding_rounds",
    "funding_total_usd",
    "milestones",
    "has_VC",
    "has_angel",
    "has_roundA",
    "has_roundB",
    "has_roundC",
    "has_roundD",
    "avg_participants",
    "is_top500"
]

X = df[features]

#convert target coloumn
y = df["status"].map({
    "acquired": 1,
    "closed": 0
})

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state = 42
)

#Train Random Forest model
model = RandomForestClassifier(
    n_estimators= 100,
    random_state=42
)

model.fit(X_train, y_train)

#predict on test daa
y_pred = model.predict(X_test)

print("\nRandom Forest Model Trained Successfully")
print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Save trained model and feature names
joblib.dump(model, "models/random_forest_model.pkl")
joblib.dump(features, "models/features.pkl")

print("\nModel saved successfully")
print("Saved: models/random_forest_model.pkl")
print("Saved: models/features.pkl")