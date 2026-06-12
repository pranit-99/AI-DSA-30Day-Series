from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import joblib



df = pd.read_csv("data/incidents.csv")

X = df["description"]
y = df["category"]

print(X.head())
print(y.head())


#Converting Text into Numbers
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

#Train Naive Bayes
model  = MultinomialNB()
model.fit(X_vectorized, y)

print(X_vectorized.shape)

#Testing Our First Prediction
test_incident = ["Database connection failed after deployment"]
test_vector = vectorizer.transform(test_incident)
prediction = model.predict(test_vector)
print("Prediction", prediction[0])
#Basic Testing Ends

#----------testing few more Cases---------------
samples = [
    "Multiple failed login attempts detected",
    "VPN tunnel disconnected unexpectedly",
    "Frontend application crashed",
    "Database service unavailable"
]

sample_vectors = vectorizer.transform(samples)

predictions = model.predict(sample_vectors)

for text, category in zip(samples, predictions):
    print(f"{text} --> {category}")
#---------Testing Few More Cases Ends-----------


import joblib

joblib.dump(model, "models/naive_bayes_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")
