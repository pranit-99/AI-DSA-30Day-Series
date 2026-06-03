import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (accuracy_score,
                             precision_score,
                             recall_score,
                             f1_score,
                             classification_report
                             )

def get_model_metrics():
    data = pd.read_csv("bug_training_data.csv")

    X = data["description"]
    y = data["priority"]

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y, 
                                                    test_size=0.25,
                                                    random_state=42,
                                                    stratify = y
                                                    )
    vectorizer = TfidfVectorizer()

    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_vectorized, y_train)

    y_pred = model.predict(X_test_vectorized)
    accuracy = accuracy_score(y_test, y_pred)

    print("Model Accuracy:", accuracy)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    return {
        "accuracy": round(accuracy * 100, 2),
        "precision": round(
            precision_score(y_test, y_pred, average="weighted", zero_division=0) * 100, 2
        ),
        "recall": round(
            recall_score(y_test, y_pred, average="weighted", zero_division=0) * 100, 2
        ),
        "f1_score": round(
            f1_score(y_test, y_pred, average="weighted", zero_division=0) * 100, 2
        )
    }

if __name__ == "__main__":
    metrics = get_model_metrics()
    print(metrics)

