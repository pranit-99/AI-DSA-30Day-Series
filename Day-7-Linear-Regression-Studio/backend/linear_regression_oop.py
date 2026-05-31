#We will implement Linear Regression from Scartch for better Understanding
import math
import csv

class LinearRegressionBuilding:
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values
        self.mean_x = 0
        self.mean_y = 0
        self.slope = 0
        self.numerator = 0
        self.denominator = 0
        self.intercept = 0
        self.calculation_table = []
        self.mae = 0
        self.mse = 0
        self.rmse = 0
        self.r2_score = 0


    def display_dataset(self):
        print("Dataset:")
        print("Hours Studied (X) | Marks (Y)")

        for x,y in zip(self.x_values, self.y_values):
            print(f"{x} | {y}")

    #Before Linear Regression model can learn the line, first we have to find center of the data
    #Find mean of x_values  and y_values
    #We stored Mean as Object Varialbes so that it will be used repeatedly when calculating
    def calculate_means(self):
        self.mean_x = sum(self.x_values) / len(self.x_values)
        self.mean_y = sum(self.y_values) / len(self.y_values)
        print("---------------------")
        print("/\nMean Calculations")
        print("------------------------")
        print(f"Mean X = {self.mean_x}")
        print(f"Mean Y = {self.mean_y}")

    #After Calculating mean we will create a basic calculation table
    def create_calculation_table(self):
        print("---------------------")
        print("\nCalculation Table")
        print("---------------------")
        print("X | Y | X-meanX | Y-meanY | Product | X-meanX Squared")

        for x,y in zip(self.x_values, self.y_values):
            x_difference = x - self.mean_x
            y_difference = y - self.mean_y
            product = x_difference * y_difference
            x_difference_squared = x_difference ** 2

            row = {
            "x": x,
            "y": y,
            "x_difference": x_difference,
            "y_difference": y_difference,
            "product": product,
            "x_difference_squared": x_difference_squared
            }

            self.calculation_table.append(row)

            print(
            f"{x} | {y} | {x_difference} | {y_difference} | "
            f"{product} | {x_difference_squared}")

    #After we get all values in calculation table we will Calculate Slope (b₁)
    def calculate_slope(self):
        self.numerator = sum(
                row["product"]
                for row in self.calculation_table
                )
        
        self.denominator = sum(
                row["x_difference_squared"]
                for row in self.calculation_table
                )
            
        self.slope = self.numerator / self.denominator
        print("------------------------")
        print("\nSlope Calculation")
        print("------------------------")
        print(f"Numerator = {self.numerator}")
        print(f"Denominator = {self.denominator}")
        print(f"Slope (b1) = {self.slope}")
    
    #After Getting slope successfully we will calculate intercept b0 = mean_y - (b1 × mean_x)
    def calculate_intercept(self):
        self.intercept = self.mean_y - (self.slope * self.mean_x)
        print("------------------------")
        print("\nIntercept Calculation")
        print("------------------------")
        print(f"Intercept (b0) = {self.intercept}")

    #Now we will create a predection function
    def predict(self, x):
        predicted_y = self.intercept + (self.slope * x)
        
        return predicted_y
    
    #Following function will check predicted values against Actual value
    def evaluate_training_data(self):
        print("\nTraining Data Evaluation")
        print("------------------------------------------------")
        print("X | Actual Y | Predicted Y | Error")

        self.errors = []
        for x, actual_y in zip(self.x_values, self.y_values):
            predicted_y = self.predict(x)
            error = actual_y - predicted_y
            self.errors.append(error)
            print(
                f"{x} | "
                f"{actual_y} | "
                f"{round(predicted_y, 2)} | "
                f"{round(error, 2)}"
                )
            
    #After Our model is trined we will calculate some other equation which tells some important aspects of ouw model
    #MAE = Mean Absolute Error, It tells us the average prediction mistake.
    def calculate_MAE(self):
        absolute_errors = [abs(error) for error in self.errors]
        self.mae = sum(absolute_errors) / len(absolute_errors)
        print(f"MAE = {round(self.mae, 2)}")
        return self.mae

    #MSE Mean Squared Error, Looks at Two prediction mistakes, MSE is the reason the regression formula exists.
    def calculate_MSE(self):
        squared_errors = [
            error ** 2
            for error in self.errors
        ]

        self.mse = sum(squared_errors) / len(squared_errors)

        print("\nMSE Calculation")
        print("------------------------")
        print(f"Squared Errors = {squared_errors}")
        print(f"MSE = {round(self.mse, 2)}")

        return self.mse
    
    #RMSE = Root Mean Squared Error, Our model prediction is typically off by around 0.69 marks.
    def calculate_rmse(self):
        mse = self.calculate_MSE()
        self.rmse = math.sqrt(mse)
        print(f"RMSE = {round(self.rmse, 2)}")
        return self.rmse
    
    #Calculate R² Score, How much of the variation in Y is explained by X
    def calculate_r2_score(self):
        sse = sum(error ** 2 for error in self.errors)
        sst = sum((y - self.mean_y) ** 2 for y in self.y_values)
        self.r2_score = 1 - (sse / sst)
        print(f"R2 Score = {round(self.r2_score, 2)}")
        return self.r2_score
    
    def train(self):
        self.calculate_means()
        self.create_calculation_table()
        self.calculate_slope()
        self.calculate_intercept()
        self.display_regression_equation()

    def evaluate(self):
        self.evaluate_training_data()
        self.calculate_MAE()
        #self.calculate_MSE()
        self.calculate_rmse()
        self.calculate_r2_score()
    
    #Add Regression Equation Display
    def display_regression_equation(self):
        print("\nFinal Regression Equation")
        print("------------------------")
        print(f"y = {round(self.intercept, 2)} + {round(self.slope, 2)}x")

    #Chart Data
    def get_chart_data(self):
        chart_data=[]

        for x, actual_y in zip(self.x_values, self.y_values):
            predicted_y = self.predict(x)

            chart_data.append({
                "x":x,
                "actual":actual_y,
                "predicted":round(predicted_y, 2)
            })

        return chart_data
    
    def get_manual_results(self):
        return {
            "mean_x": round(self.mean_x, 2),
            "mean_y": round(self.mean_y, 2),
            "calculation_table": self.calculation_table,
            "slope": round(self.slope, 2),
            "intercept": round(self.intercept, 2),
            "equation": f"y = {round(self.intercept, 2)} + {round(self.slope, 2)}x",
            "mae": round(self.mae, 2),
            "mse": round(self.mse, 2),
            "rmse": round(self.rmse, 2),
            "r2_score": round(self.r2_score, 2)
        }
    
#Load Data From CSV
def load_data_from_csv(file_path):
    x_values = []
    y_values = []

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if "hours" not in row or "marks" not in row:
                raise ValueError("CSV must contain 'hours' and 'marks' columns")

            try:
                x_values.append(float(row["hours"]))
                y_values.append(float(row["marks"]))
            except ValueError:
                raise ValueError("Hours and marks must be numeric values")

    if len(x_values) == 0:
        raise ValueError("CSV file is empty")

    if len(x_values) != len(y_values):
        raise ValueError("X and Y values count does not match")

    return x_values, y_values



try:

#Step 1:- Create a basic dataset
#x_values = [1, 2, 3, 4, 5] #Hours Studied
#y_values = [2, 4, 5, 4, 5] # Marks Scored
    x_values, y_values = load_data_from_csv("student_marks.csv")
#Here we will create object of class
    model = LinearRegressionBuilding(x_values, y_values)

#Display Dataset
    model.display_dataset()
    model.train()
    new_hours = 6
    predicted_marks = model.predict(new_hours)
    print("\nNew Prediction")
    print("------------------------")
    print(f"Hours Studied = {new_hours}")
    print(f"Predicted Marks = {predicted_marks}")
    model.evaluate()

except ValueError as error:
    print(f"Error:{error}")


