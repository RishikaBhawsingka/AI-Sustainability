
from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd

from backend.routes.gpu import GPUInput
from backend.routes.thermal import ThermalInput
from backend.models.model_loader import gpu_model, tlhc_model

from backend.services.shap_service import (
    explain_gpu,
    explain_thermal
)

from backend.services.rag_service import retrieve
from backend.services.llm_service import generate_recommendation


router = APIRouter()


class AnalysisInput(BaseModel):
    gpu: GPUInput
    thermal: ThermalInput


@router.post("/analyze")
def analyze(data: AnalysisInput):

    # =========================================================
    # 1. GPU POWER PREDICTION
    # =========================================================

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


    # =========================================================
    # 2. THERMAL / TLHC PREDICTION
    # =========================================================

    thermal_features = [[
        data.thermal.P_ac_0,
        data.thermal.P_ac_1,
        data.thermal.P_ac_2,
        data.thermal.P_ac_3,
        data.thermal.P_ac_4,
        data.thermal.P_ac_5,
        data.thermal.P_ac_6,
        data.thermal.P_ac_7,

        data.thermal.P_cu_0,
        data.thermal.P_cu_1,
        data.thermal.P_cu_2,
        data.thermal.P_cu_3,
        data.thermal.P_cu_4,
        data.thermal.P_cu_5,
        data.thermal.P_cu_6,
        data.thermal.P_cu_7,

        data.thermal.T_out_0,
        data.thermal.T_out_1,
        data.thermal.T_out_2,
        data.thermal.T_out_3,
        data.thermal.T_out_4,
        data.thermal.T_out_5,
        data.thermal.T_out_6,
        data.thermal.T_out_7,

        data.thermal.T_MEAS_0,
        data.thermal.T_MEAS_1,
        data.thermal.T_MEAS_2,
        data.thermal.T_MEAS_3,
        data.thermal.T_MEAS_4,
        data.thermal.T_MEAS_5,
        data.thermal.T_MEAS_6,
        data.thermal.T_MEAS_7,

        data.thermal.T_celCC_0,
        data.thermal.T_celCC_1,
        data.thermal.T_celCC_2,
        data.thermal.T_celCC_3,
        data.thermal.T_celCC_4,
        data.thermal.T_celCC_5,
        data.thermal.T_celCC_6,
        data.thermal.T_celCC_7,

        data.thermal.DoW,
        data.thermal.WeH
    ]]

    thermal_prediction = tlhc_model.predict(thermal_features)[0]


    # =========================================================
    # 3. SHAP EXPLANATIONS
    # =========================================================

    gpu_feature_names = [
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

    thermal_feature_names = [
        "P_ac_0", "P_ac_1",
        "P_ac_2", "P_ac_3",
        "P_ac_4", "P_ac_5",
        "P_ac_6", "P_ac_7",

        "P_cu_0", "P_cu_1",
        "P_cu_2", "P_cu_3",
        "P_cu_4", "P_cu_5",
        "P_cu_6", "P_cu_7",

        "T_out_0", "T_out_1",
        "T_out_2", "T_out_3",
        "T_out_4", "T_out_5",
        "T_out_6", "T_out_7",

        "T_MEAS_0", "T_MEAS_1",
        "T_MEAS_2", "T_MEAS_3",
        "T_MEAS_4", "T_MEAS_5",
        "T_MEAS_6", "T_MEAS_7",

        "T_celCC_0", "T_celCC_1",
        "T_celCC_2", "T_celCC_3",
        "T_celCC_4", "T_celCC_5",
        "T_celCC_6", "T_celCC_7",

        "DoW",
        "WeH"
    ]

    gpu_explanation = explain_gpu(
        gpu_features,
        gpu_feature_names
    )

    thermal_explanation = explain_thermal(
        thermal_features,
        thermal_feature_names
    )


    # =========================================================
    # 4. COOLING TOWER DATASET
    # =========================================================

    cooling_df = pd.read_csv(
        "ml/data/raw/cooling_tower_dataset.csv"
    )
    baseline_water = float(
    cooling_df["Water Consumption (L)"].mean()
    )

    reference_savings = float(
    cooling_df["Energy Savings (%)"].mean()
    )

    illustrative_water_saving = (
    baseline_water * reference_savings / 100
    )

    cooling_data = {
      "water_consumption_liters": round(baseline_water, 2),
      "energy_consumption_kwh": round(
        float(cooling_df["Energy Consumption (kWh)"].mean()), 2
      ),
      "cooling_capacity_kw": round(
        float(cooling_df["Cooling Capacity (kW)"].mean()), 2
     ),
       "cooling_efficiency_percent": round(
        float(cooling_df["Cooling Tower Efficiency (%)"].mean()), 2
      ),
      "energy_savings_percent": round(reference_savings, 2),
      "co2_emissions_kg": round(
        float(cooling_df["CO2 Emissions (kg)"].mean()), 2
      ),

    # Illustrative scenario, NOT measured saving
    "illustrative_water_saving_liters": round(
        illustrative_water_saving, 2
    )
   }
    


    # =========================================================
    # 5. RAG
    # =========================================================

    query = (
        "GPU power thermal load cooling efficiency "
        "water consumption energy optimization"
    )

    retrieved_context = retrieve(
        query,
        top_k=3
    )


    # =========================================================
    # 6. GROQ LLM RECOMMENDATION
    # =========================================================

    recommendation = generate_recommendation(
        gpu_power=round(
            float(gpu_prediction),
            2
        ),

        tlhc=round(
            float(thermal_prediction),
            4
        ),

        gpu_explanation=gpu_explanation,

        thermal_explanation=thermal_explanation,

        cooling_data=cooling_data,

        retrieved_context=retrieved_context
    )


    # =========================================================
    # 7. FINAL RESPONSE
    # =========================================================

    return {
        "gpu_power_watts": round(
            float(gpu_prediction),
            2
        ),

        "tlhc_standardized": round(
            float(thermal_prediction),
            4
        ),

        "gpu_explanation": gpu_explanation,

        "thermal_explanation": thermal_explanation,

        "cooling_data": cooling_data,

        "rag_context": retrieved_context,

        "recommendation": recommendation
    }

