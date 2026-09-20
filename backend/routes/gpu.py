from fastapi import APIRouter
from pydantic import BaseModel
from backend.models.model_loader import gpu_model

router = APIRouter()


class GPUInput(BaseModel):
    avgmemoryutilization_pct: float
    avgsmutilization_pct: float
    memoryutilization_pct_avg: float
    memoryutilization_pct_max: float
    memoryutilization_pct_min: float
    pcierxbandwidth_megabytes_avg: float
    pcierxbandwidth_megabytes_max: float
    pcierxbandwidth_megabytes_min: float
    pcietxbandwidth_megabytes_avg: float
    pcietxbandwidth_megabytes_max: float
    pcietxbandwidth_megabytes_min: float
    totalexecutiontime_sec: float


@router.post("/predict/gpu-power")
def predict_gpu_power(data: GPUInput):

    features = [[
        data.avgmemoryutilization_pct,
        data.avgsmutilization_pct,
        data.memoryutilization_pct_avg,
        data.memoryutilization_pct_max,
        data.memoryutilization_pct_min,
        data.pcierxbandwidth_megabytes_avg,
        data.pcierxbandwidth_megabytes_max,
        data.pcierxbandwidth_megabytes_min,
        data.pcietxbandwidth_megabytes_avg,
        data.pcietxbandwidth_megabytes_max,
        data.pcietxbandwidth_megabytes_min,
        data.totalexecutiontime_sec
    ]]

    prediction = gpu_model.predict(features)[0]

    return {
        "predicted_gpu_power_watts": round(float(prediction), 2)
    }