import { useEffect, useState } from "react";
import "../css/Dashboard.css";
import PredictionChart from "../components/charts/PredictionChart";

// Recharts
import { LineChart, Line, ResponsiveContainer } from "recharts";

// Existing UI components
import HealthSummary from "../components/Summary/HealthSummary";
import InsightCard from "../components/Insight/InsightCard";
import ErrorAnalysis from "../components/Analytics/ErrorAnalysis";

// 🔥 API SERVICE
import {
  getActualVsPredicted,
  getFutureForecast,
} from "../services/predictionService";

const PredictionDashboard = () => {

  const [chartData, setChartData] = useState([]);
  const [forecastData, setForecastData] = useState([]);
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const past = await getActualVsPredicted();
      const future = await getFutureForecast();

      if (past) {
        setChartData(past.data);
        setKpis(past.kpis);
      }

      setForecastData(future);
    };

    fetchData();
  }, []);

  if (!kpis) {
    return <div className="dashboard">Loading...</div>;
  }

  // KPI cards → Jan–Mar
  const kpiData = chartData.slice(0, 3);

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
          <PredictionChart data={chartData} />
        </div>

        {/* RIGHT PANEL */}
        <div className="right-panel">

          <ErrorAnalysis data={chartData} />

          <div className="changes-card">
            <h4>Key Changes This Month</h4>

            <div className="change-item">
              <span className="change-dot green"></span>
              Ticket trends adjusted based on latest model output.
            </div>

            <div className="change-item">
              <span className="change-dot blue"></span>
              Forecast accuracy: {kpis.accuracy}%.
            </div>

            <div className="change-item">
              <span className="change-dot orange"></span>
              Error margin: {kpis.mape}%.
            </div>

            <button className="report-btn">
              View Detailed Report →
            </button>
          </div>

        </div>

      </div>

      {/* ===== FORECAST (LIVE DATA) ===== */}
      <div className="forecast-card">

        <div className="forecast-header">
          <div>
            <h3>Future Forecast</h3>
            <span className="forecast-sub">Next 3 Months</span>
          </div>
        </div>

        {forecastData.map((item, index) => {

          const width = (item.predicted / 3000) * 100; // normalize
          const isPositive = true;

          return (
            <div className="forecast-row-new" key={index}>

              <div className="forecast-month">{item.month}</div>

              <div className="forecast-bar-wrapper">
                <div className="forecast-bar-bg">
                  <div
                    className="forecast-bar-fill"
                    style={{ width: `${width}%` }}
                  ></div>
                </div>
              </div>

              <div className="forecast-value">
                {item.predicted.toLocaleString()}
              </div>

              <div className="forecast-range">
                {(item.predicted * 0.95).toFixed(0)} – {(item.predicted * 1.05).toFixed(0)}
              </div>

              <div className="forecast-change green">
                + forecast
              </div>

              <div className="forecast-trend green">
                ↑
              </div>

            </div>
          );
        })}

        <div className="forecast-note">
          ℹ Forecasts are generated using ML model predictions.
        </div>

      </div>

    </div>
  );
};

export default PredictionDashboard;