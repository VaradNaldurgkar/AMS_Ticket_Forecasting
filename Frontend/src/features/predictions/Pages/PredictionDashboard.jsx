import { useEffect, useState } from "react";
import "../css/Dashboard.css";
import PredictionChart from "../components/charts/PredictionChart";

// Recharts
import {
  LineChart,
  Line,
  ResponsiveContainer,
} from "recharts";

// Existing UI components
import HealthSummary from "../components/Summary/HealthSummary";
import ErrorAnalysis from "../components/Analytics/ErrorAnalysis";

// API SERVICES
import {
  getActualVsPredicted,
  getFutureForecast,
} from "../services/predictionService";

const PredictionDashboard = () => {

  const [chartData, setChartData] = useState([]);
  const [forecastData, setForecastData] = useState([]);
  const [showAllMonths, setShowAllMonths] =
    useState(false);

  const [kpis, setKpis] = useState({
    accuracy: 95.78,
    mape: 4.22,
  });

  // ====================================================
  // FETCH DATA
  // ====================================================

  useEffect(() => {

    const fetchData = async () => {

      try {

        const past =
          await getActualVsPredicted();

        const future =
          await getFutureForecast();

        if (past && past.data) {

          setChartData(past.data);

          const avgErrorPercentage =
            past.data.reduce(
              (sum, item) =>
                sum +
                (
                  Math.abs(
                    item.actual -
                    item.predicted
                  ) /
                  item.actual
                ) *
                100,
              0
            ) / past.data.length;

          const accuracy = (
            100 - avgErrorPercentage
          ).toFixed(2);

          setKpis({
            accuracy,
            mape:
              avgErrorPercentage.toFixed(2),
          });
        }

        if (future) {
          setForecastData(future);
        }

      } catch (error) {

        console.error(
          "Dashboard Error:",
          error
        );
      }
    };

    fetchData();

  }, []);

  // ====================================================
  // LOADING
  // ====================================================

  if (!chartData.length) {

    return (
      <div className="dashboard">
        Loading...
      </div>
    );
  }

  // ====================================================
  // SHOW LATEST 4 MONTHS ONLY
  // ====================================================

  const visibleChartData =
    showAllMonths
      ? chartData
      : chartData.slice(-4);

  return (

    <div className="dashboard">

      {/* PAGE HEADER */}

      <div className="prediction-page-header">

        <h1 className="prediction-title">
          Prediction Analytics
        </h1>

        <p className="prediction-subtitle">
          Historical trends, forecasting accuracy and future ticket predictions
        </p>

      </div>

      <HealthSummary data={chartData} />

{/* SHOW MORE BUTTON */}

{chartData.length > 4 && (

  <div
    style={{
      display: "flex",
      justifyContent: "flex-end",
      alignItems: "center",
      marginTop: "10px",
      marginBottom: "12px",
      paddingRight: "5px",
    }}
  >
    <button
      onClick={() =>
        setShowAllMonths(
          !showAllMonths
        )
      }
      style={{
        padding: "8px 16px",
        fontSize: "13px",
        fontWeight: "600",
        borderRadius: "8px",
        border: "1px solid #d1d5db",
        background: "#ffffff",
        color: "#374151",
        cursor: "pointer",
        transition: "all 0.2s ease",
      }}
    >
      {showAllMonths
        ? "Show Less"
        : "Show More"}
    </button>
  </div>

)}

{/* KPI CARDS */}

<div className="kpi-row">

        {visibleChartData.map((item, index) => {

          const error = Math.abs(
            item.actual - item.predicted
          );

          const deviation = (
            (error / item.actual) * 100
          ).toFixed(1);

          const isHigh = deviation > 2;

          const trendData = [
            { v: item.actual * 0.9 },
            { v: item.actual * 1.05 },
            { v: item.actual * 0.95 },
            { v: item.actual * 1.1 },
            { v: item.actual },
          ];

          return (

            <div
              className="kpi-card month-card"
              key={index}
            >

              <div className="kpi-header">
                {item.month}
              </div>

              <div className="kpi-body">

                <div className="kpi-main">

                  <div>
                    <span className="kpi-label">
                      Actual
                    </span>

                    <span className="kpi-value">
                      {item.actual}
                    </span>
                  </div>

                  <div style={{ textAlign: "right" }}>
                    <span className="kpi-label">
                      Predicted
                    </span>

                    <span className="kpi-value">
                      {item.predicted}
                    </span>
                  </div>

                </div>

                <div
                  className={`kpi-deviation ${
                    isHigh ? "kpi-red" : "kpi-green"
                  }`}
                >
                  {isHigh ? "↓" : "↑"} {deviation}%
                </div>

                <div className="kpi-sparkline">

                  <ResponsiveContainer
                    width="100%"
                    height={60}
                  >

                    <LineChart data={trendData}>

                      <Line
                        type="monotone"
                        dataKey="v"
                        stroke={
                          isHigh
                            ? "#dc2626"
                            : "#16a34a"
                        }
                        strokeWidth={2.5}
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

      </div>


      {/* MAIN ANALYTICS GRID */}

      <div className="analytics-grid">

        <div className="chart-container">

          <h3>
            Actual vs Predicted Tickets
          </h3>

          <PredictionChart data={chartData} />

        </div>

        <div className="right-panel">

          <ErrorAnalysis data={chartData} />

          <div className="changes-card">

            <h4>
              Key Changes This Month
            </h4>

            <div className="change-item">
            <span className="change-dot change-green"></span>
              Historical forecast evaluation stabilized.
            </div>

            <div className="change-item">
              <span className="change-dot blue"></span>
              Forecast accuracy: {kpis.accuracy}%.
            </div>

            <div className="change-item">
              <span className="change-dot orange"></span>
              Error margin: {kpis.mape}%.
            </div>

            

          </div>

        </div>

      </div>

      {/* FUTURE FORECAST */}

      <div className="forecast-card">

        <div className="forecast-header">

          <div>

            <h3>
              Future Forecast
            </h3>

            <span className="forecast-sub">
              Next 3 Months
            </span>

          </div>

        </div>

        {forecastData.map((item, index) => {

          const width =
            (item.predicted / 3000) * 100;

          return (

            <div
              className="forecast-row-new"
              key={index}
            >

              <div className="forecast-month">
                {item.month}
              </div>

              <div className="forecast-bar-wrapper">

                <div className="forecast-bar-bg">

                  <div
                    className="forecast-bar-fill"
                    style={{
                      width: `${width}%`
                    }}
                  ></div>

                </div>

              </div>

              <div className="forecast-value">
                {item.predicted.toLocaleString()}
              </div>

              <div className="forecast-range">

                {(item.predicted * 0.95).toFixed(0)}
                {" – "}
                {(item.predicted * 1.05).toFixed(0)}

              </div>

              <div className="forecast-change forecast-green">
                + forecast
              </div>

              <div className="forecast-trend forecast-green">
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