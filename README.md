# 🌱 AquaTherma AI

### AI-Driven Cooling & Sustainability Intelligence for Data Centers

AquaTherma AI is an **AI-driven sustainability decision-support system** that helps analyze data-center workload, GPU power usage, thermal behavior, and cooling-resource opportunities.

It combines **Machine Learning, Explainable AI (SHAP), Retrieval-Augmented Generation (RAG), and LLM-based recommendations** into a single interactive dashboard.

> **Workload → Prediction → Explainability → Cooling Intelligence → Sustainability Insight → AI Recommendation**

---

## 🚀 What Does AquaTherma AI Do?

Data centers generate significant computational workloads and heat, creating challenges around **energy efficiency, thermal management, and cooling resources**.

AquaTherma AI provides a unified intelligence layer that:

* ⚡ Predicts GPU power usage from workload and utilization metrics
* 🌡️ Predicts a standardized thermal load indicator
* 🔍 Explains model predictions using SHAP
* 💧 Uses cooling-tower data as sustainability reference information
* 📚 Retrieves relevant cooling/sustainability knowledge using RAG
* 🤖 Generates structured technical recommendations using an LLM
* 📊 Presents the complete analysis through an interactive React dashboard

---

## 🧠 System Architecture

```text
                 GPU Workload
                      │
                      ▼
             ┌─────────────────┐
             │  ML Prediction  │
             └────────┬────────┘
                      │
             ┌────────┴────────┐
             ▼                 ▼
       GPU Power          Thermal Load
       Prediction         Prediction
             │                 │
             └────────┬────────┘
                      ▼
              ┌───────────────┐
              │ SHAP Explain. │
              └───────┬───────┘
                      │
                      ▼
          Cooling Reference Data
                      │
                      ▼
               Sustainability
                  Insights
                      │
             ┌────────┴────────┐
             ▼                 ▼
            RAG               LLM
        Knowledge      Recommendations
             │                 │
             └────────┬────────┘
                      ▼
              React Dashboard
```

---

## 📊 Datasets

### 1. `final_dataset_std.csv`

A standardized dataset containing thermal and system-related features.

Used to train the **TLHC thermal load prediction model**.

* **27,013 samples**
* **42 predictor features**
* Model: Random Forest Regressor
* R²: **0.9583**
* MAE: **0.1423**

> TLHC is treated as a standardized model target and is not interpreted directly as temperature in °C.

### 2. `dcgm.csv`

Contains GPU/DCGM utilization and power-related metrics.

Used to predict **average GPU power usage**.

* **96,893 samples**
* **22 predictor features**
* Model: Random Forest Regressor
* R²: **0.9833**
* MAE: **3.79 W**

### 3. `cooling_tower_dataset.csv`

Contains cooling-system reference information such as:

* Water consumption
* Energy consumption
* Cooling capacity
* Cooling-tower efficiency
* Energy savings
* CO₂ emissions

This dataset is used as **contextual sustainability reference data**, rather than as a direct real-time water-consumption prediction model.

---

## 🔍 Explainable AI

AquaTherma AI uses **SHAP (SHapley Additive exPlanations)** to understand which features influence the ML predictions.

This helps move beyond:

> "The model predicted this value."

towards:

> "These features had the strongest influence on the prediction."

SHAP visualizations are provided for both the GPU power and thermal prediction models.

---

## 💧 Water Optimization Layer

The dashboard combines cooling-tower reference information with the analysis pipeline to present a sustainability perspective.

The displayed water-saving figure is an **illustrative optimization opportunity derived from reference data**, not a measured real-world saving or live water-consumption prediction.

This distinction keeps the system focused on **decision support rather than direct physical control**.

---

## 📚 RAG + LLM Intelligence

The system includes a Retrieval-Augmented Generation pipeline.

```text
ML Results
    +
SHAP Insights
    +
Cooling Data
    +
Retrieved Knowledge
        ↓
      LLM
        ↓
Structured Recommendation
```

The LLM converts technical model outputs and retrieved knowledge into structured sections such as:

* Assessment
* Key Drivers
* Sustainability Insight
* Recommended Actions

---

## 🖥️ Interactive Dashboard

The React dashboard allows users to:

1. Adjust simulated GPU workload
2. Run AI analysis
3. View predicted GPU power
4. View thermal load prediction
5. Explore SHAP explanations
6. Inspect cooling-system reference metrics
7. View the illustrative water-optimization opportunity
8. Receive AI-generated recommendations

---

## 🛠️ Tech Stack

### Machine Learning

* Python
* Pandas
* Scikit-learn
* Random Forest
* SHAP
* Joblib

### Backend

* FastAPI
* Python
* RAG pipeline
* Groq LLM

### Frontend

* React
* Vite
* JavaScript
* CSS

### Data & Development

* CSV datasets
* MySQL
* Git
* GitHub
* VS Code

---

## 📁 Project Structure

```text
AquaTherma-AI/
│
├── backend/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── rag/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── ml/
│   ├── data/
│   │   └── raw/
│   ├── models/
│   ├── preprocessing.py
│   ├── train.py
│   └── predict.py
│
├── rag/
│   ├── ingest.py
│   └── rag_pipeline.py
│
├── database/
│   └── schema.sql
│
├── simulation/
│   └── generate_data.py
│
├── report.md
├── .gitignore
└── README.md
```

---

## ⚙️ Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/RishikaBhawsingka/AI-Sustainability.git
cd AI-Sustainability
```

### 2. Backend

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Start FastAPI:

```bash
uvicorn backend.main:app --reload
```

Backend will run on:

```text
http://127.0.0.1:8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔐 Environment Variables

Create a `.env` file for API credentials where required.

Example:

```env
GROQ_API_KEY=your_api_key_here
```

**Never commit API keys or `.env` files to GitHub.**

---

## 📈 Model Performance

| Model                   | Target            |         R² |        MAE |
| ----------------------- | ----------------- | ---------: | ---------: |
| GPU Power Random Forest | Average GPU Power | **0.9833** | **3.79 W** |
| Thermal Random Forest   | Standardized TLHC | **0.9583** | **0.1423** |

These results are based on the project's train/test evaluation and should not be interpreted as guaranteed real-world performance.

---

## 🎯 Project Goal

AquaTherma AI aims to demonstrate how **AI, explainability, retrieval systems, and sustainability data can work together** to support more informed data-center cooling and resource-efficiency decisions.

The system is designed as a **decision-support prototype**, not an autonomous cooling-control system.

---

## 🔮 Future Scope

* Real-time data-center telemetry integration
* Larger and more diverse cooling datasets
* Time-series forecasting
* Real-time water-consumption modeling
* Digital-twin simulation
* Automated anomaly detection
* Integration with data-center monitoring systems
* Optimization models for workload scheduling and cooling resources

---

## 👩‍💻 Author

**Rishika Bhawsingka**

B.Tech Computer Science & Engineering

---

### 🌱 AquaTherma AI

**Making data-center intelligence more explainable, sustainable, and actionable.**
