import mlflow
from mlflow.models import infer_signature

import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

mlflow.set_tracking_uri("http://localhost:8086")
# Load the Iris dataset
X, y = datasets.load_iris(return_X_y=True)
# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define the model hyperparameters
params = {
    "solver": "lbfgs",
    "max_iter": 1000,
    "multi_class": "auto",
    "random_state": 8888,
}
# Train the model
lr = LogisticRegression(**params)
lr.fit(X_train, y_train)

# Predict on the test set
y_pred = lr.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)

mlflow.set_experiment("iris experiment")
with mlflow.start_run(run_name="iris run") as run:
    # log params
    mlflow.log_params(params)
    # log metrics
    mlflow.log_metric("accuracy", accuracy)
    # set tag
    mlflow.set_tag("model", "LogisticRegression")
    # infer signature
    signature = infer_signature(X_train, lr.predict(X_train))
    # save model
    model_info = mlflow.sklearn.log_model(
        lr,
        artifact_path="iris_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="iris_model",
    )

    print(f"Model saved to {model_info.model_uri}")