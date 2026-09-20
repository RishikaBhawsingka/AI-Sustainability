from fastapi import APIRouter
import pandas as pd

router = APIRouter()

DATA_PATH = "ml/data/raw/cooling_tower_dataset.csv"


@router.get("/cooling/summary")
def cooling_summary():

    df = pd.read_csv(DATA_PATH)

    return {
        "records": len(df),

        "water_consumption_liters": round(
            float(df["Water Consumption (L)"].mean()), 2
        ),

        "energy_consumption_kwh": round(
            float(df["Energy Consumption (kWh)"].mean()), 2
        ),

        "cooling_capacity_kw": round(
            float(df["Cooling Capacity (kW)"].mean()), 2
        ),

        "cooling_efficiency_percent": round(
            float(df["Cooling Tower Efficiency (%)"].mean()), 2
        ),

        "energy_savings_percent": round(
            float(df["Energy Savings (%)"].mean()), 2
        ),

        "co2_emissions_kg": round(
            float(df["CO2 Emissions (kg)"].mean()), 2
        )
    }