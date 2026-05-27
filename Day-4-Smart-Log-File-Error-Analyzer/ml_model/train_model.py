import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

data = pd.read_csv("training_data.csv")

X = data["error_message"]
y = data["severity"]

vectorizer = TfidfVectorizer()

X_vectorized = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vectorized, y)

with open("vectorizer.pkl", "wb") as file:
    pickle.dump(vectorizer, file)

with open("severity_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Severity prediction model trained and saved successfully.")