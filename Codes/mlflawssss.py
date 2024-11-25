import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import json
import joblib
from scipy.stats import randint

# Load a dataset
data = load_iris()
X = data.data
y = data.target

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to DataFrame with feature names for model training
X_train_df = pd.DataFrame(X_train, columns=data.feature_names)
X_test_df = pd.DataFrame(X_test, columns=data.feature_names)

# Scaling the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_df)
X_test_scaled = scaler.transform(X_test_df)

# Start MLflow experiment
with mlflow.start_run():
    # Initialize a model
    model = RandomForestClassifier(random_state=42)

    # Hyperparameter tuning using RandomizedSearchCV
    param_dist = {"n_estimators": randint(10, 100), "max_depth": randint(1, 20)}
    random_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=10, random_state=42)
    random_search.fit(X_train_scaled, y_train)
    
    # Best parameters found by RandomizedSearchCV
    best_model = random_search.best_estimator_
    print(f"Best parameters found: {random_search.best_params_}")
    
    # Cross-validation
    cross_val_scores = cross_val_score(best_model, X_train_scaled, y_train, cv=5)
    print(f"Cross-validation scores: {cross_val_scores}")
    mlflow.log_metric("mean_cross_val_score", cross_val_scores.mean())

    # Train the model with the best parameters
    best_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = best_model.predict(X_test_scaled)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    mlflow.log_metric("accuracy", accuracy)

    # Confusion matrix and classification report
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred)
    print(f"Confusion Matrix:\n{cm}")
    print(f"Classification Report:\n{cr}")
    mlflow.log_param("confusion_matrix", cm)
    mlflow.log_param("classification_report", cr)

    # ROC Curve and AUC
    fpr, tpr, thresholds = roc_curve(y_test, best_model.predict_proba(X_test_scaled)[:, 1], pos_label=1)
    roc_auc = auc(fpr, tpr)
    print(f"AUC: {roc_auc}")

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()
    mlflow.log_artifact("roc_curve.png")

    # Feature importance plot
    feature_importances = best_model.feature_importances_
    plt.barh(data.feature_names, feature_importances)
    plt.xlabel("Feature Importance")
    plt.title("Feature Importance in Random Forest Model")
    plt.savefig("feature_importance_plot.png")
    mlflow.log_artifact("feature_importance_plot.png")

    # Save the trained model locally
    joblib.dump(best_model, 'random_forest_model.pkl')
    mlflow.log_artifact('random_forest_model.pkl')

    # Log model to MLflow
    input_example = pd.DataFrame(X_test_scaled[:5], columns=data.feature_names)  # First 5 rows of the test set
    mlflow.sklearn.log_model(best_model, "random_forest_model", input_example=input_example)

    # Save hyperparameter tuning results
    tuning_results = {
        'best_params': random_search.best_params_,
        'best_score': random_search.best_score_,
        'all_results': random_search.cv_results_
    }

    with open("tuning_results.json", "w") as f:
        json.dump(tuning_results, f)
    mlflow.log_artifact("tuning_results.json")
