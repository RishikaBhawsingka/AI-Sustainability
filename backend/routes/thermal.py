from fastapi import APIRouter
from pydantic import BaseModel
from backend.models.model_loader import tlhc_model

router = APIRouter()


class ThermalInput(BaseModel):
    P_ac_0: float
    P_ac_1: float
    P_ac_2: float
    P_ac_3: float
    P_ac_4: float
    P_ac_5: float
    P_ac_6: float
    P_ac_7: float

    P_cu_0: float
    P_cu_1: float
    P_cu_2: float
    P_cu_3: float
    P_cu_4: float
    P_cu_5: float
    P_cu_6: float
    P_cu_7: float

    T_out_0: float
    T_out_1: float
    T_out_2: float
    T_out_3: float
    T_out_4: float
    T_out_5: float
    T_out_6: float
    T_out_7: float

    T_MEAS_0: float
    T_MEAS_1: float
    T_MEAS_2: float
    T_MEAS_3: float
    T_MEAS_4: float
    T_MEAS_5: float
    T_MEAS_6: float
    T_MEAS_7: float

    T_celCC_0: float
    T_celCC_1: float
    T_celCC_2: float
    T_celCC_3: float
    T_celCC_4: float
    T_celCC_5: float
    T_celCC_6: float
    T_celCC_7: float

    DoW: float
    WeH: float


@router.post("/predict/thermal")
def predict_thermal(data: ThermalInput):

    features = [[
        data.P_ac_0, data.P_ac_1, data.P_ac_2, data.P_ac_3,
        data.P_ac_4, data.P_ac_5, data.P_ac_6, data.P_ac_7,

        data.P_cu_0, data.P_cu_1, data.P_cu_2, data.P_cu_3,
        data.P_cu_4, data.P_cu_5, data.P_cu_6, data.P_cu_7,

        data.T_out_0, data.T_out_1, data.T_out_2, data.T_out_3,
        data.T_out_4, data.T_out_5, data.T_out_6, data.T_out_7,

        data.T_MEAS_0, data.T_MEAS_1, data.T_MEAS_2, data.T_MEAS_3,
        data.T_MEAS_4, data.T_MEAS_5, data.T_MEAS_6, data.T_MEAS_7,

        data.T_celCC_0, data.T_celCC_1, data.T_celCC_2, data.T_celCC_3,
        data.T_celCC_4, data.T_celCC_5, data.T_celCC_6, data.T_celCC_7,

        data.DoW,
        data.WeH
    ]]

    prediction = tlhc_model.predict(features)[0]

    return {
        "predicted_tlhc": round(float(prediction), 4)
    }