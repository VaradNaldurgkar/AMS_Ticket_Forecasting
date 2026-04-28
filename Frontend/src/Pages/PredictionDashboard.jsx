import "../css/Dashboard.css";
import PredictionChart from "../components/charts/PredictionChart";
import { predictionData } from "../data/sampleData";

// Recharts
import { LineChart, Line, ResponsiveContainer } from "recharts";

// Existing
import HealthSummary from "../components/Summary/HealthSummary";
import InsightCard from "../components/Insight/InsightCard";

// Error Analysis
import ErrorAnalysis from "../components/Analytics/ErrorAnalysis";

const PredictionDashboard = () => {

  const kpiData = predictionData.slice(0, 3);

  const forecastData = [
    { month: "May '26", value: 2870, percent: "+4%", width: 65 },
    { month: "Jun '26", value: 2990, percent: "+6%", width: 75 },
    { month: "Jul '26", value: 2680, percent: "+9%", width: 60 },
  ];

  return (
    <div className="dashboard">

      {/* HEALTH SUMMARY */}
      <HealthSummary />

      {/* KPI ROW */}
      <div className="kpi-row">
        {kpiData.map((item, index) => {

          const error = Math.abs(item.actual - item.predicted);
          const deviation = ((error / item.actual) * 100).toFixed(1);
          const isHigh = deviation > 2;

          const trendData = [
            { v: item.actual * 0.9 },
            { v: item.actual * 1.05 },
            { v: item.actual * 0.95 },
            { v: item.actual * 1.1 },
            { v: item.actual },
          ];

          return (
            <div className="kpi-card month-card" key={index}>
              <div className="kpi-header">{item.month}</div>

              <div className="kpi-body">

                <div className="kpi-main">
                  <div>
                    <span className="kpi-label">Actual</span>
                    <span className="kpi-value">{item.actual}</span>
                  </div>

                  <div>
                    <span className="kpi-label">Predicted</span>
                    <span className="kpi-value">{item.predicted}</span>
                  </div>
                </div>

                <div className={`kpi-deviation ${isHigh ? "red" : "green"}`}>
                  {isHigh ? "↓" : "↑"} {deviation}%
                </div>

                <div className="kpi-sparkline">
                  <ResponsiveContainer width="100%" height={60}>
                    <LineChart data={trendData}>
                      <Line
                        type="monotone"
                        dataKey="v"
                        stroke={isHigh ? "#dc2626" : "#16a34a"}
                        strokeWidth={2}
                        dot={false}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

              </div>

              <div className="kpi-footer">
                Error: {error.toFixed(0)} tickets
              </div>
            </div>
          );
        })}

        <InsightCard />
      </div>

      {/* MAIN ANALYTICS GRID */}
      <div className="analytics-grid">

        {/* LEFT: CHART */}
        <div className="chart-container">
          <h3>Actual vs Predicted Tickets</h3>
          <PredictionChart data={predictionData} />
        </div>

        {/* RIGHT PANEL */}
        <div className="right-panel">

          <ErrorAnalysis data={predictionData} />

          <div className="changes-card">
            <h4>Key Changes This Month</h4>

            <div className="change-item">
              <span className="change-dot green"></span>
              Ticket volume decreased by 12% compared to March.
            </div>

            <div className="change-item">
              <span className="change-dot blue"></span>
              P1 incidents decreased by 30%.
            </div>

            <div className="change-item">
              <span className="change-dot orange"></span>
              Backend issues reduced by 18%.
            </div>

            <button className="report-btn">
              View Detailed Report →
            </button>
          </div>

        </div>

      </div>

      {/* ===== ENHANCED FORECAST ===== */}
      <div className="forecast-card">

        <div className="forecast-header">
          <div>
            <h3>3-Month Forecast</h3>
            <span className="forecast-sub">May–Jul 2026</span>
          </div>

          <div className="forecast-columns">
            <span>Forecast</span>
            <span>Confidence Range</span>
            <span>vs Previous 3M</span>
            <span>Trend</span>
          </div>
        </div>

        {forecastData.map((item, index) => {
          const isPositive = item.percent.includes("+");

          return (
            <div className="forecast-row-new" key={index}>

              <div className="forecast-month">{item.month}</div>

              <div className="forecast-bar-wrapper">
                <div className="forecast-bar-bg">
                  <div
                    className="forecast-bar-fill"
                    style={{ width: `${item.width}%` }}
                  ></div>
                </div>
              </div>

              <div className="forecast-value">
                {item.value.toLocaleString()}
              </div>

              <div className="forecast-range">
                {Math.floor(item.value * 0.95).toLocaleString()} – {Math.floor(item.value * 1.05).toLocaleString()}
              </div>

              <div className={`forecast-change ${isPositive ? "green" : "red"}`}>
                {item.percent}
              </div>

              <div className={`forecast-trend ${isPositive ? "green" : "red"}`}>
                {isPositive ? "↑" : "↓"}
              </div>

            </div>
          );
        })}

        <div className="forecast-note">
          ℹ Forecasts are based on historical data and ML model predictions with 91% confidence.
        </div>

      </div>

    </div>
  );
};

export default PredictionDashboard;