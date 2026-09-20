from fastapi import APIRouter
from backend.services.llm_service import generate_recommendation

router = APIRouter()


@router.get("/llm/test")
def llm_test():

    result = generate_recommendation(
        gpu_power=59.73,
        tlhc=-0.5755,
        gpu_explanation=[
            {
                "feature": "memoryutilization_pct_avg",
                "impact": -12.3313
            }
        ],
        thermal_explanation=[
            {
                "feature": "P_cu_0",
                "impact": -0.2056
            }
        ],
        retrieved_context=[
            {
                "text": "Higher GPU and memory utilization can be associated with higher power consumption and increased heat generation."
            },
            {
                "text": "Cooling optimization should consider both energy consumption and water consumption."
            }
        ]
    )

    return {
        "recommendation": result
    }