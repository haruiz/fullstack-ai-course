import mlflow
mlflow.set_tracking_uri("http://localhost:8086")
model_uri = 'runs:/e66e9935c8e648f0bb0909cc09b0e020/iris_model'
# This is the input example logged with the model
pyfunc_model = mlflow.pyfunc.load_model(model_uri)
input_data = pyfunc_model.input_example
print(input_data)
# Verify the model with the provided input data using the logged dependencies.
# For more details, refer to:
# https://mlflow.org/docs/latest/models.html#validate-models-before-deployment
mlflow.models.predict(
    model_uri=model_uri,
    input_data=input_data,
    env_manager="uv",
)