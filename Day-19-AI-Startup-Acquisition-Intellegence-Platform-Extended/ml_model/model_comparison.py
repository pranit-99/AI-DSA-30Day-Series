import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def get_model_comparison():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "data", "startup_data.csv")

    df = pd.read_csv(DATA_PATH)

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

    y = df["status"].map({
        "acquired": 1,
        "closed": 0
    })

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    dt_pred = dt_model.predict(X_test)
    dt_accuracy = accuracy_score(y_test, dt_pred)

    rf_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)

    improvement = ((rf_accuracy - dt_accuracy) / dt_accuracy) * 100

    return {
        "decision_tree_accuracy": round(dt_accuracy * 100, 2),
        "random_forest_accuracy": round(rf_accuracy * 100, 2),
        "accuracy_improvement": round(improvement, 2),
        "winner": "Random Forest"
    }


if __name__ == "__main__":
    result = get_model_comparison()

    print("\nModel Comparison\n")
    print(f"Decision Tree Accuracy : {result['decision_tree_accuracy']}%")
    print(f"Random Forest Accuracy : {result['random_forest_accuracy']}%")
    print(f"Accuracy Improvement : {result['accuracy_improvement']}%")
    print(f"Winner : {result['winner']}")