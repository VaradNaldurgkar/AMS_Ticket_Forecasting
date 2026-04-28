import "../css/Dashboard.css";
import PredictionChart from "../components/charts/PredictionChart";
import { predictionData } from "../data/sampleData";

// ✅ Recharts
import { LineChart, Line, ResponsiveContainer } from "recharts";

// ✅ Existing
import HealthSummary from "../components/Summary/HealthSummary";

// ✅ Insight Card
import InsightCard from "../components/Insight/InsightCard";

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

          // ✅ FIXED: Better variation for visible trend
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

                {/* ACTUAL vs PREDICTED */}
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

                {/* DEVIATION */}
                <div className={`kpi-deviation ${isHigh ? "red" : "green"}`}>
                  {isHigh ? "↓" : "↑"} {deviation}%
                </div>

                {/* ✅ FIXED: Proper sparkline */}
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

              {/* FOOTER */}
              <div className="kpi-footer">
                Error: {error.toFixed(0)} tickets
              </div>

            </div>
          );
        })}

        {/* INSIGHT CARD */}
        <InsightCard />
      </div>

      {/* CHART */}
      <div className="chart-container">
        <h3>Actual vs Predicted Tickets</h3>
        <PredictionChart data={predictionData} />
      </div>

      {/* FORECAST */}
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