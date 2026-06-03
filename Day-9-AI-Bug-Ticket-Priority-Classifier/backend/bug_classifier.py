import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class BugClassifier:
    def __init__(self):
        self.data = pd.read_csv("bug_training_data.csv")

        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()
        
        X = self.data["description"]
        y = self.data["priority"]

        X_vectorized = self.vectorizer.fit_transform(X)

        self.model.fit(X_vectorized, y)

        self.priority_numbers = {
            "Critical": 1,
            "High": 2,
            "Medium": 3,
            "Low": 4
        }

    def classify_bug(self, bug_description):
        bug_vector = self.vectorizer.transform([bug_description])
        predicted_priority = self.model.predict(bug_vector)[0]
        priority_number = self.priority_numbers[predicted_priority]
        return priority_number, predicted_priority