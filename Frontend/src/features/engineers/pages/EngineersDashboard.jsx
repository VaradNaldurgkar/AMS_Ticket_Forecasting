import "../css/EngineersDashboard.css";

import EngineersKPI from "../Components/Cards/EngineersKPI";

import HeadcountTrendChart from "../Components/Charts/HeadcountTrendChart";
import HiringTrendChart from "../Components/Charts/HiringTrendChart";
import HiringRatioChart from "../Components/Charts/HiringRatioChart";
import GrowthChart from "../Components/Charts/GrowthChart";

import ForecastCalculation from "../Components/Analytics/ForecastCalculation";
import KeyInsights from "../Components/Insights/KeyInsights";

const EngineersDashboard = () => {
  return (
    <div className="engineers-dashboard">

      {/* HEADER */}
      <div className="engineers-header">
        <div>
          <h1>Engineers Workforce Analytics & Forecast</h1>

          <p>
            Understand hiring trends and forecast future engineer requirements
          </p>
        </div>

        <div className="last-updated">
          Last Updated: June 9, 2026
        </div>
      </div>

      {/* KPI CARDS */}
      <EngineersKPI />

      {/* MAIN CONTENT */}
      <div className="engineers-main">

        {/* LEFT SIDE */}
        <div className="charts-section">

          <HeadcountTrendChart />

          <HiringTrendChart />

          <HiringRatioChart />

          <GrowthChart />

          <div className="insights-wrapper">
            <KeyInsights />
          </div>

        </div>

        {/* RIGHT SIDE */}
        <div className="forecast-wrapper">
          <ForecastCalculation />
        </div>

      </div>

    </div>
  );
};

export default EngineersDashboard;