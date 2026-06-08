from sklearn.linear_model import LogisticRegression
import numpy as np


X_train = np.array([
    [100, 1, 500, 0],
    [200, 2, 600, 0],
    [5000, 15, 10, 1],
    [8000, 20, 5, 1],
    [150, 1, 700, 0],
    [12000, 25, 2, 1]
])

y_train = np.array([
    0,
    0,
    1,
    1,
    0,
    1
])


model = LogisticRegression()
model.fit(X_train, y_train)


def predict_transaction(transaction):

    features = [[
        transaction["amount"],
        transaction["transaction_count_last_hour"],
        transaction["account_age_days"],
        transaction["location_mismatch"]
    ]]

    fraud_probability = model.predict_proba(features)[0][1]

    prediction = model.predict(features)[0]

    return {
        "prediction": "Fraud" if prediction == 1 else "Legitimate",
        "fraud_probability": round(float(fraud_probability), 2)
    }