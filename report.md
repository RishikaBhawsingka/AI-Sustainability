### AquaTherma AI

## Overview

AquaTherma AI is an AI-driven sustainability decision-support system designed to help understand data-center workload, thermal behavior, power usage, and cooling-resource opportunities. It combines Machine Learning, Explainable AI, RAG, and LLM-based recommendations in an interactive dashboard.
### Datasets

* **DCGM Dataset:** Contains GPU utilization, memory utilization, power usage, energy consumption, and job execution data for analyzing computing workload and power demand.
* **Data Center Temperature Dataset:** Contains computing-unit/AC power and multiple temperature measurements for modeling data-center thermal behavior.
* **Cooling Tower Dataset:** Contains cooling capacity, water consumption, water flow, energy consumption, efficiency, and CO₂ emissions for cooling and resource-impact analysis.
* These datasets are used as **complementary sources for separate modules** of AquaTherma AI rather than being directly merged row-by-row.

Dataset 2 — Cooling Tower Operational Dataset: A clean 1,000-record dataset containing cooling, water, energy, control, efficiency, savings, and emissions variables. Exploratory analysis showed weak relationships between water consumption and the available operational features, so it will be treated as an operational/reference dataset rather than forcing an ML water-consumption prediction task.

Dataset 3 — GPU Power Prediction
Dataset: dcgm.csv
Records: 96,893
Target: powerusage_watts_avg
Model: Random Forest Regressor
MAE: 3.79 W
RMSE: 6.59 W
R²: 0.9833
Key finding: GPU memory/SM utilization showed strong relationships with power usage, enabling accurate GPU power prediction.
Model saved: ml/models/gpu_power_random_forest.pkl
Actual vs Predicted: The predictions closely follow the increasing trend of actual GPU power values, indicating strong agreement between observed and predicted power consumption.

Residual Analysis: The model showed near-zero mean residual (-0.026 W) with an MAE of 3.79 W, indicating low overall prediction bias and good accuracy. A maximum error of 103.52 W indicates a small number of larger prediction deviations.

SHAP Analysis: GPU and memory utilization were the dominant factors influencing power prediction. Higher utilization generally increased predicted GPU power, while PCIe bandwidth features had comparatively smaller contributions. This indicates that workload intensity is the primary driver captured by the model.


### ML Model
Dataset: final_dataset_std.csv (Data Centre Warm Channel Temperature Prediction Dataset)
Trained a Random Forest Regression model to predict TLHC (hot-corridor temperature), achieving R² = 0.9583, MAE = 0.1423, and RMSE = 0.2038.

## Datasets & ML

### 1. `final_dataset_std.csv`

Contains standardized thermal and system-related features. A Random Forest Regressor was trained to predict **TLHC (thermal load indicator)**.

* Samples: 27,013
* Features: 42 predictors
* R²: **0.9583**
* MAE: **0.1423**

### 2. `dcgm.csv`

Contains GPU/DCGM utilization and power-related metrics. A Random Forest model predicts **average GPU power usage**.

* Samples: 96,893
* Features: 22 predictors
* R²: **0.9833**
* MAE: **3.79 W**

### 3. `cooling_tower_dataset.csv`

Contains cooling-tower operational reference data including water consumption, energy consumption, cooling capacity, efficiency, energy savings, and CO₂ emissions. This dataset is used as **contextual sustainability reference data**, not as a direct water-prediction model.

## Explainable AI

SHAP is used to identify which features most influence GPU power and thermal predictions, making the ML outputs more interpretable.

## RAG + LLM

Relevant sustainability and cooling knowledge is retrieved through a RAG pipeline and combined with model outputs. A Groq-hosted LLM converts these results into structured technical recommendations.

## Dashboard

The React dashboard allows simulated GPU workload changes, runs the complete analysis pipeline, displays predictions and SHAP explanations, presents cooling-resource insights, and shows an **illustrative water-saving opportunity** based on reference data.

## Technology

**Python, FastAPI, Random Forest, SHAP, RAG, Groq LLM, React, Vite, MySQL, Git/GitHub.**

