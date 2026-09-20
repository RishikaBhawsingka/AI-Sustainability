import joblib

gpu_model = joblib.load(
    "ml/models/gpu_power_random_forest.pkl"
)

tlhc_model = joblib.load(
    "ml/models/tlhc_random_forest.pkl"
)