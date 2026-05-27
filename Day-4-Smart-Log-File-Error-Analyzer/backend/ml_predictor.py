import pickle

def load_model():
    with open("../ml_model/vectorizer.pkl", "rb") as file:
        vectorizer = pickle.load(file)
      
    with open("../ml_model/severity_model.pkl", "rb") as file:
        model = pickle.load(file)

    return vectorizer, model

vectorizer, model = load_model()

def predict_severity(error_message):
    error_vector = vectorizer.transform([error_message])
    prediction = model.predict(error_vector)

    return prediction[0]