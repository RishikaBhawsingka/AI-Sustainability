import shap
import numpy as np

from backend.models.model_loader import gpu_model, tlhc_model


gpu_explainer = shap.TreeExplainer(gpu_model)
tlhc_explainer = shap.TreeExplainer(tlhc_model)


def explain_gpu(features, feature_names):

    features = np.array(features)

    shap_values = gpu_explainer.shap_values(features)

    values = shap_values[0]

    explanation = []

    for name, value in zip(feature_names, values):
        explanation.append({
            "feature": name,
            "impact": round(float(value), 4)
        })

    explanation.sort(
        key=lambda x: abs(x["impact"]),
        reverse=True
    )

    return explanation[:5]


def explain_thermal(features, feature_names):

    features = np.array(features)

    shap_values = tlhc_explainer.shap_values(features)

    values = shap_values[0]

    explanation = []

    for name, value in zip(feature_names, values):
        explanation.append({
            "feature": name,
            "impact": round(float(value), 4)
        })

    explanation.sort(
        key=lambda x: abs(x["impact"]),
        reverse=True
    )

    return explanation[:5]