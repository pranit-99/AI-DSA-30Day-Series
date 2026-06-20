import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from tree_structure import TreeNode, print_tree, predict_with_path
import joblib


# Step 1: Load dataset
df = pd.read_csv("data/startup_data.csv")

print("Dataset Loaded Successfully")
print("Original Shape:", df.shape)


# Step 2: Select useful columns
selected_columns = [
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
    "is_top500",
    "status"
]

df = df[selected_columns]

print("Selected Shape:", df.shape)


# Step 3: Convert target column manually
df["status"] = df["status"].map({
    "acquired": 1,
    "closed": 0
})

print("\nTarget Values:")
print(df["status"].value_counts())


# Step 4: Check missing values
print("\nMissing Values:")
print(df.isnull().sum())


# Step 5: Separate input and output
X = df.drop("status", axis=1)
y = df["status"]

print("\nInput Shape:", X.shape)
print("Target Shape:", y.shape)

print("\nFirst 5 Input Rows:")
print(X.head())

print("\nFirst 5 Target Values:")
print(y.head())

# Step 6: Manual train-test split

split_index = int(0.8 * len(df))

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)

print("Training Target Shape:", y_train.shape)
print("Testing Target Shape:", y_test.shape)

# Step 7: Train Decision Tree Model

model = DecisionTreeClassifier(
    criterion="gini",
    max_depth=4,
    random_state=42
)

model.fit(X_train, y_train)

print("\nDecision Tree Model Trained Successfully")


# Step 8: Prediction

y_pred = model.predict(X_test)

print("\nPredicted Values:")
print(y_pred[:10])

print("\nActual Values:")
print(y_test.head(10).values)


# Step 9: Model Evaluation

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Step 10: Save Model

joblib.dump(model, "../backend/models/model.pkl")

print("\nModel saved successfully in backend/models/model.pkl")

# Step 11: Convert sklearn Decision Tree into custom Binary Tree

feature_names = X.columns.tolist()


def build_custom_tree(tree, node_id=0):
    feature_index = tree.feature[node_id]

    # Leaf node
    if feature_index == -2:
        prediction_value = tree.value[node_id][0]

        if prediction_value[1] > prediction_value[0]:
            prediction = "Acquired"
        else:
            prediction = "Closed"

        return TreeNode(value=prediction)

    feature_name = feature_names[feature_index]
    threshold = tree.threshold[node_id]

    left_child = build_custom_tree(tree, tree.children_left[node_id])
    right_child = build_custom_tree(tree, tree.children_right[node_id])

    return TreeNode(
        feature=feature_name,
        threshold=round(threshold, 2),
        left=left_child,
        right=right_child
    )


custom_tree_root = build_custom_tree(model.tree_)

print("\nCustom Binary Tree Representation:")
print_tree(custom_tree_root)

# Step 12: Test custom Binary Tree traversal on one startup

sample_startup = X_test.iloc[0].to_dict()

prediction, path = predict_with_path(custom_tree_root, sample_startup)

print("\nCustom Binary Tree Prediction Path:")
for step in path:
    print(step)

print("\nCustom Tree Final Prediction:", prediction)

# Step 13: Save model and feature names

joblib.dump(model, "../backend/models/model.pkl")
joblib.dump(feature_names, "../backend/models/features.pkl")

print("\nModel saved successfully in backend/models/model.pkl")
print("Feature names saved successfully in backend/models/features.pkl")