
import pandas as pd
import matplotlib.pyplot as plt
import shap
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# 1. Load dataset
df = pd.read_csv(
    "ml/data/raw/final_dataset_std.csv",
    sep=";"
)

print("Dataset shape:", df.shape)


# 2. Separate input and target
X = df.drop("TLHC", axis=1)
y = df["TLHC"]


# 3. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 4. Create model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# 5. Train
print("\nTraining model...")
model.fit(X_train, y_train)

print("Training completed!")


# 6. Predict
y_pred = model.predict(X_test)


# 7. Evaluate
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)


print("\n===== MODEL RESULTS =====")
print("MAE :", mae)
print("RMSE:", rmse)
print("R²  :", r2)


# 8. Target distribution
print("\n===== TARGET DISTRIBUTION =====")

print("Training TLHC:")
print(y_train.describe())

print("\nTesting TLHC:")
print(y_test.describe())


# 9. Simple baseline
baseline_pred = [y_train.mean()] * len(y_test)

baseline_mae = mean_absolute_error(y_test, baseline_pred)
baseline_rmse = mean_squared_error(y_test, baseline_pred) ** 0.5
baseline_r2 = r2_score(y_test, baseline_pred)

print("\n===== BASELINE RESULTS =====")
print("Baseline MAE :", baseline_mae)
print("Baseline RMSE:", baseline_rmse)
print("Baseline R²  :", baseline_r2)


# 10. Actual vs Predicted Plot
plt.figure(figsize=(8, 6))

plt.scatter(y_test, y_pred, alpha=0.5)

# Perfect prediction line
min_value = min(y_test.min(), y_pred.min())
max_value = max(y_test.max(), y_pred.max())

plt.plot(
    [min_value, max_value],
    [min_value, max_value],
    linestyle="--"
)

plt.xlabel("Actual TLHC")
plt.ylabel("Predicted TLHC")
plt.title("Actual vs Predicted TLHC")

plt.tight_layout()
plt.show()

# 11. Residual Analysis

residuals = y_test - y_pred

print("\n===== RESIDUAL ANALYSIS =====")
print("Mean Residual:", residuals.mean())
print("Residual Std :", residuals.std())
print("Max Error    :", residuals.abs().max())
print("Mean Abs Error:", residuals.abs().mean())


# Residual Plot
plt.figure(figsize=(8, 6))

plt.scatter(y_pred, residuals, alpha=0.5)

# Zero-error line
plt.axhline(y=0, linestyle="--")

plt.xlabel("Predicted TLHC")
plt.ylabel("Residual (Actual - Predicted)")
plt.title("Residual Analysis - TLHC Prediction")

plt.tight_layout()
plt.show()

# 12. SHAP Explainability

print("\n===== SHAP ANALYSIS =====")

# Use a smaller sample for explanation
X_shap = X_test.sample(
    n=50,
    random_state=42
)

# Use TreeExplainer
explainer = shap.TreeExplainer(model)

print("Calculating SHAP values...")

shap_values = explainer.shap_values(X_shap)

print("SHAP analysis completed!")

# SHAP Summary Plot
shap.summary_plot(
    shap_values,
    X_shap,
    show=False
)

plt.title("SHAP Feature Importance - TLHC Prediction")
plt.tight_layout()
plt.show()



# Save trained model
joblib.dump(model, "ml/models/tlhc_random_forest.pkl")

print("\nModel saved successfully!")