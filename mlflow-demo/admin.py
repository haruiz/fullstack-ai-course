import mlflow
mlflow.set_tracking_uri("http://localhost:8086")

all_runs = mlflow.search_runs(
    search_all_experiments=True,
    filter_string="metrics.accuracy > 0.9",
    order_by=["metrics.accuracy DESC"],
)
for run_index, run_info in all_runs.iterrows():
    print(run_info["metrics.accuracy"], run_info["run_id"])