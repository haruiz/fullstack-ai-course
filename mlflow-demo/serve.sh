export MLFLOW_TRACKING_URI=http://localhost:8086
uv run mlflow models serve -m "runs:/e66e9935c8e648f0bb0909cc09b0e020/iris_model" -p 5000 --env-manager uv