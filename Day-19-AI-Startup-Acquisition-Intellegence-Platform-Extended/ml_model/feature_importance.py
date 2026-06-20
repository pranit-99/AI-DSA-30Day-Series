import joblib
import os
import pandas as pd


def get_feature_importance():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "models", "random_forest_model.pkl")
    FEATURES_PATH = os.path.join(BASE_DIR, "models", "features.pkl")

    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)

    importance_scores = model.feature_importances_

    importance_df = pd.DataFrame({
        "feature": features,
        "importance": importance_scores
    })

    importance_df = importance_df.sort_values(
        by="importance",
        ascending=False
    )

    top_features = importance_df.head(5)

    result = []

    for _, row in top_features.iterrows():
        result.append({
            "feature": row["feature"],
            "importance": round(row["importance"] * 100, 2)
        })

    return result


if __name__ == "__main__":
    print("\nTop 5 Startup Acquisition Factors:\n")

    for item in get_feature_importance():
        print(f"{item['feature']} : {item['importance']}%")