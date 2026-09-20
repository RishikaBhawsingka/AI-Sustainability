import { useState } from "react";
import axios from "axios";
import "./index.css";

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const [gpuMemory, setGpuMemory] = useState(10);
  const [gpuSM, setGpuSM] = useState(20);

  const runAnalysis = async () => {
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/analyze",
        {
          gpu: {
            avgmemoryutilization_pct: gpuMemory,
            avgsmutilization_pct: gpuSM,
            memoryutilization_pct_avg: gpuMemory,
            memoryutilization_pct_max: gpuMemory,
            memoryutilization_pct_min: gpuMemory,

            pcierxbandwidth_megabytes_avg: 1000,
            pcierxbandwidth_megabytes_max: 1200,
            pcierxbandwidth_megabytes_min: 800,

            pcietxbandwidth_megabytes_avg: 800,
            pcietxbandwidth_megabytes_max: 1000,
            pcietxbandwidth_megabytes_min: 600,

            totalexecutiontime_sec: 200
          },

          thermal: {
            ...Object.fromEntries(
              [
                "P_ac",
                "P_cu",
                "T_out",
                "T_MEAS",
                "T_celCC"
              ].flatMap(prefix =>
                Array.from(
                  { length: 8 },
                  (_, i) => [`${prefix}_${i}`, 0]
                )
              )
            ),

            DoW: 0,
            WeH: 0
          }
        }
      );

      setResult(response.data);

    } catch (error) {
      console.error(error);
      alert("Could not connect to Aquatherma backend.");
    }

    setLoading(false);
  };


  /* ================================
     LLM RESPONSE PARSER
  ================================= */

  const parseRecommendation = (text) => {
    if (!text) return null;

    const clean = text.replace(/\r/g, "").trim();

    const getSection = (start, ends = []) => {
      const startIndex = clean
        .toLowerCase()
        .indexOf(start.toLowerCase());

      if (startIndex === -1) return "";

      let contentStart = startIndex + start.length;
      let endIndex = clean.length;

      ends.forEach(end => {
        const index = clean
          .toLowerCase()
          .indexOf(end.toLowerCase(), contentStart);

        if (index !== -1 && index < endIndex) {
          endIndex = index;
        }
      });

      return clean
        .slice(contentStart, endIndex)
        .trim();
    };

    return {
      assessment: getSection("ASSESSMENT", [
        "KEY DRIVERS",
        "SUSTAINABILITY INSIGHT",
        "RECOMMENDED ACTIONS"
      ]),

      drivers: getSection("KEY DRIVERS", [
        "SUSTAINABILITY INSIGHT",
        "RECOMMENDED ACTIONS"
      ]),

      sustainability: getSection(
        "SUSTAINABILITY INSIGHT",
        ["RECOMMENDED ACTIONS"]
      ),

      actions: getSection("RECOMMENDED ACTIONS")
    };
  };


  const recommendation =
    result?.recommendation
      ? parseRecommendation(result.recommendation)
      : null;


  const cleanBulletText = (text) => {
    if (!text) return [];

    return text
      .split(/\n|(?=•)|(?=\*)/)
      .map(line =>
        line
          .replace(/^[-•*]\s*/, "")
          .trim()
      )
      .filter(Boolean);
  };


  const cleanActions = (text) => {
    if (!text) return [];

    const normalized = text
      .replace(/\r/g, "")
      .replace(/RECOMMENDED ACTIONS:?/gi, "")
      .trim();

    const numbered = normalized.match(
      /\d+[\.\)]\s*.*?(?=\s+\d+[\.\)]|$)/g
    );

    if (numbered && numbered.length > 0) {
      return numbered
        .map(item =>
          item
            .replace(/^\d+[\.\)]\s*/, "")
            .trim()
        )
        .filter(Boolean);
    }

    return normalized
      .split(/\n|•|(?<=\.)\s+(?=[A-Z])/)
      .map(item =>
        item
          .replace(/^[-*]\s*/, "")
          .trim()
      )
      .filter(Boolean)
      .slice(0, 3);
  };


  /* ================================
     FEATURE NAME FORMATTER
  ================================= */

  const gpuFeatureName = (feature) => {
    return feature
      .replace(
        "memoryutilization_pct_avg",
        "Memory Utilization Average"
      )
      .replace(
        "avgmemoryutilization_pct",
        "Average Memory Utilization"
      )
      .replace(
        "avgsmutilization_pct",
        "Average SM Utilization"
      )
      .replace(
        "memoryutilization_pct_max",
        "Maximum Memory Utilization"
      )
      .replace(
        "memoryutilization_pct_min",
        "Minimum Memory Utilization"
      )
      .replace(
        "pcierxbandwidth_megabytes_avg",
        "Average PCIe RX Bandwidth"
      )
      .replace(
        "pcierxbandwidth_megabytes_max",
        "Maximum PCIe RX Bandwidth"
      )
      .replace(
        "pcierxbandwidth_megabytes_min",
        "Minimum PCIe RX Bandwidth"
      )
      .replace(
        "pcietxbandwidth_megabytes_avg",
        "Average PCIe TX Bandwidth"
      )
      .replace(
        "pcietxbandwidth_megabytes_max",
        "Maximum PCIe TX Bandwidth"
      )
      .replace(
        "pcietxbandwidth_megabytes_min",
        "Minimum PCIe TX Bandwidth"
      )
      .replace(
        "totalexecutiontime_sec",
        "Total Execution Time"
      );
  };


  const thermalFeatureName = (feature) => {
    return feature
      .replace(/^P_ac_/, "AC Power ")
      .replace(/^P_cu_/, "Cooling Unit Power ")
      .replace(/^T_out_/, "Outdoor Temperature ")
      .replace(/^T_MEAS_/, "Measured Temperature ")
      .replace(/^T_celCC_/, "Cell Cooling Temperature ")
      .replace(/^DoW$/, "Day of Week")
      .replace(/^WeH$/, "Week Hour");
  };


  /* ================================
     RENDER
  ================================= */

  return (
    <div className="app">

      {/* HEADER */}

      <header>

        <div className="brand">
          <div className="brand-mark">
            A
          </div>

          <div>
            <h1>Aquatherma AI</h1>
            <p>
              AI-powered cooling intelligence for data centers
            </p>
          </div>
        </div>

        <div className="status">
          <span></span>
          Backend Online
        </div>

      </header>


      <main>

        {/* HERO */}

        <section className="hero">

          <div className="hero-copy">

            <span className="eyebrow">
              AI · SUSTAINABILITY · DATA CENTER
            </span>

            <h2>
              Cooling Intelligence
              <br />
              Dashboard
            </h2>

            <p>
              Predict workload-related power demand,
              understand model decisions, and generate
              sustainability insights.
            </p>

          </div>


          <div className="workload-control">

            <div className="control-heading">
              <div>
                <span>SIMULATED WORKLOAD</span>
                <strong>
                  GPU workload parameters
                </strong>
              </div>

              <div className="workload-badge">
                {Math.round((gpuMemory + gpuSM) / 2)}%
              </div>
            </div>


            <div className="slider-row">

              <label>
                <span>Memory Utilization</span>

                <strong>{gpuMemory}%</strong>
              </label>

              <input
                type="range"
                value={gpuMemory}
                onChange={(e) =>
                  setGpuMemory(Number(e.target.value))
                }
                min="0"
                max="100"
              />

            </div>


            <div className="slider-row">

              <label>
                <span>SM Utilization</span>

                <strong>{gpuSM}%</strong>
              </label>

              <input
                type="range"
                value={gpuSM}
                onChange={(e) =>
                  setGpuSM(Number(e.target.value))
                }
                min="0"
                max="100"
              />

            </div>


            <button
              onClick={runAnalysis}
              disabled={loading}
            >
              {loading
                ? "Analyzing..."
                : "Run AI Analysis →"}
            </button>

          </div>

        </section>


        {result && (
          <>

            {/* KPI CARDS */}

            <section className="cards">

              <div className="card metric-card">

                <div className="metric-top">
                  <span>GPU POWER</span>
                  <span className="metric-icon">⚡</span>
                </div>

                <strong>
                  {result.gpu_power_watts}
                  <small> W</small>
                </strong>

                <p>
                  Predicted from simulated workload
                </p>

              </div>


              <div className="card metric-card">

                <div className="metric-top">
                  <span>TLHC SCORE</span>
                  <span className="metric-icon">◌</span>
                </div>

                <strong>
                  {result.tlhc_standardized}
                </strong>

                <p>
                  Standardized thermal-load prediction
                </p>

              </div>


              <div className="card metric-card">

                <div className="metric-top">
                  <span>WATER REFERENCE</span>
                  <span className="metric-icon">◍</span>
                </div>

                <strong>
                  {result.cooling_data.water_consumption_liters}
                  <small> L</small>
                </strong>

                <p>
                  Cooling-tower dataset average
                </p>

              </div>


              <div className="card metric-card">

                <div className="metric-top">
                  <span>COOLING EFFICIENCY</span>
                  <span className="metric-icon">✦</span>
                </div>

                <strong>
                  {result.cooling_data.cooling_efficiency_percent}
                  <small>%</small>
                </strong>

                <p>
                  Cooling-tower dataset reference
                </p>

              </div>

            </section>


            {/* WORKLOAD VISUAL */}

            <section className="visual-grid">

              <div className="panel workload-chart">

                <div className="panel-heading">

                  <div>
                    <span className="section-label">
                      WORKLOAD PROFILE
                    </span>

                    <h3>
                      Current GPU Workload
                    </h3>
                  </div>

                  <span className="live-dot">
                    ● LIVE SIMULATION
                  </span>

                </div>


                <div className="workload-visual">

                  <div className="workload-bar">

                    <div className="bar-label">
                      <span>Memory</span>
                      <strong>{gpuMemory}%</strong>
                    </div>

                    <div className="bar-track">
                      <div
                        className="bar-fill"
                        style={{
                          width: `${gpuMemory}%`
                        }}
                      />
                    </div>

                  </div>


                  <div className="workload-bar">

                    <div className="bar-label">
                      <span>SM Utilization</span>
                      <strong>{gpuSM}%</strong>
                    </div>

                    <div className="bar-track">
                      <div
                        className="bar-fill secondary"
                        style={{
                          width: `${gpuSM}%`
                        }}
                      />
                    </div>

                  </div>


                  <div className="power-output">

                    <span>
                      PREDICTED GPU POWER
                    </span>

                    <strong>
                      {result.gpu_power_watts} W
                    </strong>

                  </div>

                </div>

              </div>


              {/* COOLING VISUAL */}

              <div className="panel resource-panel">

                <div className="panel-heading">

                  <div>
                    <span className="section-label">
                      RESOURCE DATA
                    </span>

                    <h3>
                      Cooling Tower
                    </h3>
                  </div>

                </div>


                <div className="resource-items">

                  <div className="resource-item">

                    <div className="resource-info">
                      <span>Water</span>
                      <strong>
                        {result.cooling_data.water_consumption_liters} L
                      </strong>
                    </div>

                    <div className="resource-track">
                      <div
                        style={{
                          width: "75%"
                        }}
                      />
                    </div>

                  </div>


                  <div className="resource-item">

                    <div className="resource-info">
                      <span>Energy</span>
                      <strong>
                        {result.cooling_data.energy_consumption_kwh} kWh
                      </strong>
                    </div>

                    <div className="resource-track">
                      <div
                        style={{
                          width: "62%"
                        }}
                      />
                    </div>

                  </div>


                  <div className="resource-item">

                    <div className="resource-info">
                      <span>Cooling Capacity</span>
                      <strong>
                        {result.cooling_data.cooling_capacity_kw} kW
                      </strong>
                    </div>

                    <div className="resource-track">
                      <div
                        style={{
                          width: "84%"
                        }}
                      />
                    </div>

                  </div>


                  <div className="resource-item">

                    <div className="resource-info">
                      <span>CO₂ Reference</span>
                      <strong>
                        {result.cooling_data.co2_emissions_kg} kg
                      </strong>
                    </div>

                    <div className="resource-track">
                      <div
                        style={{
                          width: "35%"
                        }}
                      />
                    </div>

                  </div>

                </div>

                <small className="reference-note">
                  Reference statistics from cooling-tower dataset
                </small>

              </div>
              <div className="panel water-panel">

  <div className="panel-heading">
    <div>
      <span className="section-label">SUSTAINABILITY INTELLIGENCE</span>
      <h3>Water Optimization</h3>
    </div>

    <span className="water-badge">💧 WATER</span>
  </div>

  <div className="water-visual">

    <div className="water-circle">
      <div>
        <strong>
          {result.cooling_data.illustrative_water_saving_liters}
        </strong>
        <span>L</span>
      </div>
      <small>potential opportunity</small>
    </div>

    <div className="water-stats">

      <div>
        <span>Reference Water Use</span>
        <strong>
          {result.cooling_data.water_consumption_liters} L
        </strong>
      </div>

      <div>
        <span>Reference Saving Scenario</span>
        <strong>
          {result.cooling_data.energy_savings_percent}%
        </strong>
      </div>

    </div>

  </div>

  <div className="water-progress">
    <div
      style={{
        width: `${Math.min(
          result.cooling_data.energy_savings_percent,
          100
        )}%`
      }}
    ></div>
  </div>

  <p className="water-note">
    Illustrative opportunity derived from the cooling-tower
    reference data. This is not a measured water saving or
    real-time prediction.
  </p>

</div>
            </section>


            {/* GPU SHAP */}

            <section className="panel">

              <div className="panel-heading">

                <div>
                  <span className="section-label">
                    EXPLAINABLE AI
                  </span>

                  <h3>
                    GPU Prediction Drivers
                  </h3>
                </div>

                <span className="shap-badge">
                  SHAP
                </span>

              </div>


              <p className="xai-description">
                SHAP explains which features contribute most
                to the model's GPU power prediction.
              </p>


              <div className="xai-legend">

                <span>
                  <i className="legend-positive"></i>
                  Pushes prediction higher
                </span>

                <span>
                  <i className="legend-negative"></i>
                  Pushes prediction lower
                </span>

              </div>


              {result.gpu_explanation.map(
                (item, index) => (

                  <div
                    className="explanation"
                    key={index}
                  >

                    <span>
                      {gpuFeatureName(item.feature)}
                    </span>

                    <div className="impact-value">

                      <div
                        className={
                          item.impact >= 0
                            ? "impact-bar positive-bar"
                            : "impact-bar negative-bar"
                        }

                        style={{
                          width: `${Math.min(
                            Math.abs(item.impact) * 5,
                            100
                          )}%`
                        }}
                      />

                      <strong
                        className={
                          item.impact >= 0
                            ? "positive-impact"
                            : "negative-impact"
                        }
                      >
                        {item.impact >= 0
                          ? "+"
                          : ""}
                        {item.impact}
                      </strong>

                    </div>

                  </div>

                )
              )}

            </section>


            {/* THERMAL SHAP */}

            <section className="panel">

              <div className="panel-heading">

                <div>
                  <span className="section-label">
                    EXPLAINABLE AI
                  </span>

                  <h3>
                    Thermal Prediction Drivers
                  </h3>
                </div>

                <span className="shap-badge">
                  SHAP
                </span>

              </div>


              <p className="xai-description">
                SHAP shows which thermal and environmental
                features influence the standardized TLHC prediction.
              </p>


              <div className="xai-legend">

                <span>
                  <i className="legend-positive"></i>
                  Pushes prediction higher
                </span>

                <span>
                  <i className="legend-negative"></i>
                  Pushes prediction lower
                </span>

              </div>


              {result.thermal_explanation.map(
                (item, index) => (

                  <div
                    className="explanation"
                    key={index}
                  >

                    <span>
                      {thermalFeatureName(item.feature)}
                    </span>

                    <div className="impact-value">

                      <div
                        className={
                          item.impact >= 0
                            ? "impact-bar positive-bar"
                            : "impact-bar negative-bar"
                        }

                        style={{
                          width: `${Math.min(
                            Math.abs(item.impact) * 100,
                            100
                          )}%`
                        }}
                      />

                      <strong
                        className={
                          item.impact >= 0
                            ? "positive-impact"
                            : "negative-impact"
                        }
                      >
                        {item.impact >= 0
                          ? "+"
                          : ""}
                        {item.impact}
                      </strong>

                    </div>

                  </div>

                )
              )}

            </section>


            {/* AI RECOMMENDATION */}

            {recommendation && (

              <section className="ai-section">

                <div className="ai-heading">

                  <div className="ai-icon">
                    ✦
                  </div>

                  <div>
                    <h3>
                      AI Sustainability Intelligence
                    </h3>

                    <p>
                      ML + SHAP + Cooling Data + RAG
                    </p>
                  </div>

                </div>


                <div className="ai-card assessment-card">

                  <div className="ai-card-title">
                    <span>◉</span>
                    Assessment
                  </div>

                  <p>
                    {recommendation.assessment}
                  </p>

                </div>


                <div className="ai-grid">

                  <div className="ai-card">

                    <div className="ai-card-title">
                      <span>⌁</span>
                      Key Drivers
                    </div>

                    <div className="ai-list">

                      {cleanBulletText(
                        recommendation.drivers
                      ).map((item, index) => (

                        <div
                          className="ai-list-item"
                          key={index}
                        >
                          <span>•</span>
                          <p>{item}</p>
                        </div>

                      ))}

                    </div>

                  </div>


                  <div className="ai-card">

                    <div className="ai-card-title">
                      <span>◈</span>
                      Sustainability Insight
                    </div>

                    <p>
                      {recommendation.sustainability}
                    </p>

                  </div>

                </div>


                <div className="ai-card actions-card">

                  <div className="ai-card-title">
                    <span>✓</span>
                    Recommended Actions
                  </div>

                  <div className="actions-list">

                    {cleanActions(
                      recommendation.actions
                    ).length > 0 ? (

                      cleanActions(
                        recommendation.actions
                      ).map((item, index) => (

                        <div
                          className="action-item"
                          key={index}
                        >

                          <div className="action-number">
                            {index + 1}
                          </div>

                          <p>{item}</p>

                        </div>

                      ))

                    ) : (

                      <div className="action-item">

                        <div className="action-number">
                          ✓
                        </div>

                        <p>
                          Continue monitoring GPU utilization
                          and thermal indicators during
                          changing workloads.
                        </p>

                      </div>

                    )}

                  </div>

                </div>

              </section>

            )}

          </>
        )}

      </main>

    </div>
  );
}

export default App;