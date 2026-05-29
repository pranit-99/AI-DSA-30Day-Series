import pickle

with open("productivity_model.pkl", "rb") as file:
    model = pickle.load(file)

commits = 7
bugs_resolved = 3
pull_requests = 2
code_reviews = 4

prediction = model.predict([[commits, bugs_resolved, pull_requests, code_reviews]])

print("Predicted Productive Hours:", round(prediction[0], 2))