import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv("ml/data/raw/dcgm.csv")


# ==============================
# FEATURES AND TARGET
# ==============================

features = [
    "avgmemoryutilization_pct",
    "avgsmutilization_pct",
    "memoryutilization_pct_avg",
    "memoryutilization_pct_max",
    "memoryutilization_pct_min",
    "pcierxbandwidth_megabytes_avg",
    "pcierxbandwidth_megabytes_max",
    "pcierxbandwidth_megabytes_min",
    "pcietxbandwidth_megabytes_avg",
    "pcietxbandwidth_megabytes_max",
    "pcietxbandwidth_megabytes_min",
    "totalexecutiontime_sec"
]

target = "powerusage_watts_avg"


X = df[features]
y = df[target]


# ==============================
# TRAIN TEST SPLIT
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==============================
# TRAIN RANDOM FOREST
# ==============================

print("\nTraining model...")

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training completed!")


# ==============================
# PREDICTION
# ==============================

y_pred = model.predict(X_test)


# ==============================
# MODEL RESULTS
# ==============================

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)


print("\n===== MODEL RESULTS =====")
print("MAE :", mae)
print("RMSE:", rmse)
print("R²  :", r2)

# SHAP analysis
import shap
X_shap = X_test.sample(n=50, random_state=42)

explainer = shap.TreeExplainer(model)

print("\nCalculating SHAP values...")
shap_values = explainer.shap_values(X_shap)

print("SHAP analysis completed!")

shap.summary_plot(
    shap_values,
    X_shap,
    show=False
)

plt.title("SHAP Feature Importance - GPU Power Prediction")
plt.tight_layout()
plt.show()


# ==============================
# ACTUAL VS PREDICTED
# ==============================

plt.figure(figsize=(7, 5))

plt.scatter(
    y_test,
    y_pred,
    alpha=0.5
)

plt.xlabel("Actual Power (W)")
plt.ylabel("Predicted Power (W)")
plt.title("Actual vs Predicted GPU Power")

plt.tight_layout()
plt.show()


# ==============================
# RESIDUAL ANALYSIS
# ==============================

residuals = y_test - y_pred

print("\n===== RESIDUAL ANALYSIS =====")
print("Mean Residual:", residuals.mean())
print("Residual Std:", residuals.std())
print("Max Error:", abs(residuals).max())
print("Mean Abs Error:", abs(residuals).mean())


# ==============================
# SAVE MODEL
# ==============================

joblib.dump(
    model,
    "ml/models/gpu_power_random_forest.pkl"
)

print("\nModel saved successfully!")

