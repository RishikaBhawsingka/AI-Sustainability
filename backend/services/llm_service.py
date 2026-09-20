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
    cooling_data,
    retrieved_context
):

    # Combine retrieved RAG knowledge
    context = "\n\n".join(
        item["text"]
        for item in retrieved_context
    )

    prompt = f"""
You are AquaTherma AI's sustainability intelligence assistant.

Your task is to turn the provided machine-learning results,
SHAP explanations, cooling-tower reference data, and retrieved
knowledge into a concise, useful technical insight for a dashboard.

IMPORTANT:
You are NOT controlling a real data center.
You are NOT making real-time cooling decisions.
You are providing decision-support insights based on the supplied data.

========================
MODEL PREDICTIONS
========================

GPU Power Prediction:
{gpu_power} W

TLHC Prediction:
{tlhc}

Note: TLHC is a STANDARDIZED model output.
Never describe it as degrees Celsius.

========================
GPU SHAP EXPLANATION
========================

{gpu_explanation}

========================
THERMAL SHAP EXPLANATION
========================

{thermal_explanation}

========================
COOLING-TOWER REFERENCE DATA
========================

Water Consumption:
{cooling_data["water_consumption_liters"]} L

Energy Consumption:
{cooling_data["energy_consumption_kwh"]} kWh

Cooling Capacity:
{cooling_data["cooling_capacity_kw"]} kW

Cooling Efficiency:
{cooling_data["cooling_efficiency_percent"]} %

Energy Savings:
{cooling_data["energy_savings_percent"]} %

CO2 Emissions:
{cooling_data["co2_emissions_kg"]} kg

IMPORTANT:
These are reference statistics from the cooling-tower dataset.
They are NOT real-time measurements and NOT predictions from the ML model.

========================
RETRIEVED KNOWLEDGE
========================

{context}

========================
RESPONSE FORMAT
========================

Return EXACTLY these four sections.

ASSESSMENT
Write 2 concise sentences.
Mention the predicted GPU power and TLHC.
Mention the most relevant SHAP/model factors.
Do not interpret TLHC as temperature.

KEY DRIVERS
Write 2-3 bullet points.
Explain which features are important according to SHAP.
Use phrases such as "the model indicates" or "SHAP identifies".
Do NOT claim that a feature physically causes the result.

SUSTAINABILITY INSIGHT
Write 2 concise sentences.
Connect the model results with the cooling-tower reference indicators.
Clearly distinguish reference data from predictions.
Do not call the reference values good, bad, efficient, inefficient, high,
low, or optimal unless directly supported by the supplied data.

RECOMMENDED ACTIONS
Write exactly 3 short numbered actions.
Actions should be practical monitoring or operational-review suggestions.
Examples:
- Monitor GPU utilization during higher workloads.
- Review cooling-system operation alongside workload changes.
- Track thermal indicators together with compute utilization over time.

Do NOT claim that any action will definitely reduce water consumption,
energy consumption, temperature, or cooling demand.

========================
STRICT RULES
========================

1. Never say the system is overheating or not overheating.
2. Never classify cooling demand as low, moderate, or high.
3. Never interpret TLHC as Celsius or any physical temperature.
4. Never claim SHAP features physically cause the prediction.
5. Never invent measurements, thresholds, sensor values, or facts.
6. Never present cooling-tower reference values as real-time values.
7. Never present cooling-tower values as ML predictions.
8. Never claim that the system directly controls cooling equipment.
9. Never claim that energy savings prove water efficiency.
10. Keep the response concise and technically defensible.
11. Avoid generic motivational language.
12. Use the actual numbers supplied above.
13. Recommendations must be based only on the supplied evidence.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise data-center sustainability "
                    "analyst. Follow the requested output format exactly."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    return response.choices[0].message.content.strip()