import mlflow

mlflow.set_tracking_uri("http://localhost:8086")
# structure data
mlflow.log_param("param1", 5)
mlflow.log_metric("accuracy", 0.9)
# Log an artifact (output file)
with open("output.txt", "w") as f:
    f.write("Hello world from mlflow!")
mlflow.log_artifact("output.txt")