import sys
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from linear_regression_oop import LinearRegressionBuilding, load_data_from_csv


def compare_models(file_path, prediction_input):
    x_values, y_values = load_data_from_csv(file_path)

    manual_model = LinearRegressionBuilding(x_values, y_values)
    manual_model.train()
    manual_model.evaluate()
    manual_prediction = manual_model.predict(prediction_input)

    X = np.array(x_values).reshape(-1, 1)
    Y = np.array(y_values)

    sklearn_model = LinearRegression()
    sklearn_model.fit(X, Y)

    sklearn_predictions = sklearn_model.predict(X)
    sklearn_prediction = sklearn_model.predict([[prediction_input]])[0]

    sklearn_mae = mean_absolute_error(Y, sklearn_predictions)
    sklearn_mse = mean_squared_error(Y, sklearn_predictions)
    sklearn_rmse = np.sqrt(sklearn_mse)
    sklearn_r2 = r2_score(Y, sklearn_predictions)

    print("\n==============================")
    print("Manual Model vs Scikit-Learn")
    print("==============================")

    print("\nManual Model")
    print("------------------------------")
    print(f"Slope (b1): {round(manual_model.slope, 2)}")
    print(f"Intercept (b0): {round(manual_model.intercept, 2)}")
    print(f"Prediction for {prediction_input}: {round(manual_prediction, 2)}")
    print(f"MAE: {round(manual_model.mae, 2)}")
    print(f"RMSE: {round(manual_model.rmse, 2)}")
    print(f"R2 Score: {round(manual_model.r2_score, 2)}")

    print("\nScikit-Learn Model")
    print("------------------------------")
    print(f"Slope (b1): {round(sklearn_model.coef_[0], 2)}")
    print(f"Intercept (b0): {round(sklearn_model.intercept_, 2)}")
    print(f"Prediction for {prediction_input}: {round(sklearn_prediction, 2)}")
    print(f"MAE: {round(sklearn_mae, 2)}")
    print(f"RMSE: {round(sklearn_rmse, 2)}")
    print(f"R2 Score: {round(sklearn_r2, 2)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("python compare_with_sklearn.py <csv_file_path> <prediction_input>")
        print("\nExample:")
        print("python compare_with_sklearn.py uploads/student_marks.csv 6")
    else:
        file_path = sys.argv[1]
        prediction_input = float(sys.argv[2])
        compare_models(file_path, prediction_input)