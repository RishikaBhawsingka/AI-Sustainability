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





rough 
from fastapi import APIRouter
from pydantic import BaseModel

from backend.routes.gpu import GPUInput
from backend.routes.thermal import ThermalInput
from backend.models.model_loader import gpu_model, tlhc_model
from backend.services.shap_service import (
    explain_gpu,
    explain_thermal
)

router = APIRouter()


class AnalysisInput(BaseModel):
    gpu: GPUInput
    thermal: ThermalInput


@router.post("/analyze")
def analyze(data: AnalysisInput):

    # ---------- GPU POWER ----------
    gpu_features = [[
        data.gpu.avgmemoryutilization_pct,
        data.gpu.avgsmutilization_pct,
        data.gpu.memoryutilization_pct_avg,
        data.gpu.memoryutilization_pct_max,
        data.gpu.memoryutilization_pct_min,
        data.gpu.pcierxbandwidth_megabytes_avg,
        data.gpu.pcierxbandwidth_megabytes_max,
        data.gpu.pcierxbandwidth_megabytes_min,
        data.gpu.pcietxbandwidth_megabytes_avg,
        data.gpu.pcietxbandwidth_megabytes_max,
        data.gpu.pcietxbandwidth_megabytes_min,
        data.gpu.totalexecutiontime_sec
    ]]

    gpu_prediction = gpu_model.predict(gpu_features)[0]


    # ---------- THERMAL ----------
    thermal_features = [[
        data.thermal.P_ac_0, data.thermal.P_ac_1,
        data.thermal.P_ac_2, data.thermal.P_ac_3,
        data.thermal.P_ac_4, data.thermal.P_ac_5,
        data.thermal.P_ac_6, data.thermal.P_ac_7,

        data.thermal.P_cu_0, data.thermal.P_cu_1,
        data.thermal.P_cu_2, data.thermal.P_cu_3,
        data.thermal.P_cu_4, data.thermal.P_cu_5,
        data.thermal.P_cu_6, data.thermal.P_cu_7,

        data.thermal.T_out_0, data.thermal.T_out_1,
        data.thermal.T_out_2, data.thermal.T_out_3,
        data.thermal.T_out_4, data.thermal.T_out_5,
        data.thermal.T_out_6, data.thermal.T_out_7,

        data.thermal.T_MEAS_0, data.thermal.T_MEAS_1,
        data.thermal.T_MEAS_2, data.thermal.T_MEAS_3,
        data.thermal.T_MEAS_4, data.thermal.T_MEAS_5,
        data.thermal.T_MEAS_6, data.thermal.T_MEAS_7,

        data.thermal.T_celCC_0, data.thermal.T_celCC_1,
        data.thermal.T_celCC_2, data.thermal.T_celCC_3,
        data.thermal.T_celCC_4, data.thermal.T_celCC_5,
        data.thermal.T_celCC_6, data.thermal.T_celCC_7,

        data.thermal.DoW,
        data.thermal.WeH
    ]]

    thermal_prediction = tlhc_model.predict(thermal_features)[0]

    gpu_explanation = explain_gpu(
    gpu_features,
    [
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
)

    thermal_explanation = explain_thermal(
    thermal_features,
    [
        "P_ac_0", "P_ac_1", "P_ac_2", "P_ac_3",
        "P_ac_4", "P_ac_5", "P_ac_6", "P_ac_7",

        "P_cu_0", "P_cu_1", "P_cu_2", "P_cu_3",
        "P_cu_4", "P_cu_5", "P_cu_6", "P_cu_7",

        "T_out_0", "T_out_1", "T_out_2", "T_out_3",
        "T_out_4", "T_out_5", "T_out_6", "T_out_7",

        "T_MEAS_0", "T_MEAS_1", "T_MEAS_2", "T_MEAS_3",
        "T_MEAS_4", "T_MEAS_5", "T_MEAS_6", "T_MEAS_7",

        "T_celCC_0", "T_celCC_1", "T_celCC_2", "T_celCC_3",
        "T_celCC_4", "T_celCC_5", "T_celCC_6", "T_celCC_7",

        "DoW",
        "WeH"
    ]
)


    return {
    "gpu_power_watts": round(
        float(gpu_prediction), 2
    ),

    "tlhc_standardized": round(
        float(thermal_prediction), 4
    ),

    "gpu_explanation": gpu_explanation,

    "thermal_explanation": thermal_explanation,

    "cooling_data": cooling_data,

    "rag_context": retrieved_context,

    "recommendation": recommendation
}


llm_service.py rough

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_recommendation(
    gpu_power,
    tlhc,
    gpu_explanation,
    thermal_explanation,
    retrieved_context
):

    context = "\n\n".join(
        item["text"] for item in retrieved_context
    )

    prompt = f"""
You are an AI cooling analyst for Aquatherma AI.

Use the provided ML predictions, SHAP explanations, and
retrieved knowledge to give a concise cooling insight.

ML Predictions:
GPU Power: {gpu_power} W
TLHC standardized prediction: {tlhc}

GPU SHAP Explanation:
{gpu_explanation}

Thermal SHAP Explanation:
{thermal_explanation}

Retrieved Knowledge:
{context}

Give your response in this format:

Cooling Insight:
[one short paragraph]

Recommended Action:
[one practical action]

Resource Efficiency:
[one short sentence about energy/water efficiency]

Important:
- Do not claim causation from SHAP.
- Do not interpret standardized TLHC as degrees Celsius.
- Do not invent sensor readings or measurements.
- Keep the answer practical and concise.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content