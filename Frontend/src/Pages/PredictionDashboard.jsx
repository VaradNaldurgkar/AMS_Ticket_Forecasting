import "../css/Dashboard.css";
import PredictionChart from "../components/charts/PredictionChart";
import { predictionData } from "../data/sampleData";

const PredictionDashboard = () => {

  const kpiData = predictionData.slice(0, 3);

  const forecastData = [
    { month: "May '26", value: 2870, percent: "+4%", width: 65 },
    { month: "Jun '26", value: 2990, percent: "+6%", width: 75 },
    { month: "Jul '26", value: 2680, percent: "+9%", width: 60 },
  ];

  return (
    <div className="dashboard">

      {/* KPI ROW */}
      <div className="kpi-row">
        {kpiData.map((item, index) => {
          const error = Math.abs(item.actual - item.predicted);

          return (
            <div className="kpi-card month-card" key={index}>
              <div className="kpi-header">{item.month}</div>

              <div className="kpi-body">
                <div className="kpi-block">
                  <span className="kpi-label">Actual</span>
                  <span className="kpi-value">{item.actual}</span>
                </div>

                <div className="kpi-block">
                  <span className="kpi-label">Predicted</span>
                  <span className="kpi-value">{item.predicted}</span>
                </div>
              </div>

              <div className={`kpi-footer ${error > 100 ? "high" : "low"}`}>
                Error: {error.toFixed(0)}
              </div>
            </div>
          );
        })}

        {/* APRIL INSIGHT */}
        <div className="kpi-card anomaly">
          <div className="kpi-header">April Insight</div>
          <h3 className="anomaly-title">High Deviation</h3>
          <p className="anomaly-text">Actual: 1306 vs Predicted: 2809</p>
        </div>
      </div>

      {/* CHART */}
      <div className="chart-container">
        <h3>Actual vs Predicted Tickets</h3>
        <PredictionChart data={predictionData} />
      </div>

      {/* ✅ IMPROVED FORECAST */}
      <div className="forecast-card">

        <div className="forecast-header">
          <h3>3-Month Forecast</h3>
          <span className="forecast-sub">May–Jul 2026</span>
        </div>

        {forecastData.map((item, index) => (
          <div className="forecast-row" key={index}>

            <div className="forecast-month">
              {item.month}
            </div>

            <div className="forecast-bar-bg">
              <div
                className="forecast-bar-fill"
                style={{ width: `${item.width}%` }}
              ></div>
            </div>

            <div className="forecast-right">
              <span className="forecast-value">
                {item.value.toLocaleString()}
              </span>
              <span className="forecast-change">
                {item.percent}
              </span>
            </div>

          </div>
        ))}

      </div>

    </div>
  );
};

export default PredictionDashboard;