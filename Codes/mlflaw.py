import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
import pandas as pd

# Load a dataset
data = load_iris()
X = data.data
y = data.target

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to DataFrame with feature names for model training
X_train_df = pd.DataFrame(X_train, columns=data.feature_names)

# Start MLflow experiment
with mlflow.start_run():
    # Initialize a model
    model = RandomForestClassifier(n_estimators=10)

    # Train the model with feature names
    model.fit(X_train_df, y_train)

    # Ensure X_test is of type float to avoid integer-related warnings
    X_test = X_test.astype(float)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)

    # Log the model and metrics to MLflow
    mlflow.log_param("n_estimators", 30)
    mlflow.log_metric("accuracy", accuracy)

    # Log the trained model with input example
    input_example = pd.DataFrame(X_test[:5], columns=data.feature_names)  # First 5 rows of the test set
    mlflow.sklearn.log_model(model, "random_forest_model", input_example=input_example)

    print(f"Accuracy: {accuracy}")
