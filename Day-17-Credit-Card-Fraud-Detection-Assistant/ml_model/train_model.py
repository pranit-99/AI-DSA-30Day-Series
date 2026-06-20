import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report


DATASET_PATH = "../backend/data/transactions.csv"


df = pd.read_csv(DATASET_PATH)
print("Dataset Loaded Successfully")
print("Shape:", df.shape)

features = [
    "amt",
    "category",
    "state",
    "gender",
    "city_pop"
]

target = "is_fraud"

df = df[features + [target]]
df = df.dropna()

X = df[features]
y = df[target]

numeric_features = ["amt", "city_pop"]
categorical_features = ["category", "state", "gender"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

model = KNeighborsClassifier(
    n_neighbors=5,
    metric="euclidean"
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

with open("model.pkl", "wb") as file:
    pickle.dump(pipeline, file)

print("Model saved successfully as model.pkl")