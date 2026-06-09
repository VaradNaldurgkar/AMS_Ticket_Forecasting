import "../../css/EngineersKPI.css";

import {
  FaUsers,
  FaUserPlus,
  FaChartPie,
  FaArrowTrendUp,
  FaChartLine
} from "react-icons/fa6";

const EngineersKPI = () => {
  return (
    <div className="engineers-kpi-row">

      <div className="engineers-kpi-card">

        <div className="kpi-top">
          <div>
            <h4>Current Total Headcount</h4>
          </div>

          <div className="icon-box blue">
            <FaUsers />
          </div>
        </div>

        <h2>5,100</h2>

        <p>As of 2026</p>

      </div>

      <div className="engineers-kpi-card">

        <div className="kpi-top">
          <h4>External Engineers Hired (2026)</h4>

          <div className="icon-box green">
            <FaUserPlus />
          </div>
        </div>

        <h2>38</h2>

        <p>As of 2026</p>

      </div>

      <div className="engineers-kpi-card">

        <div className="kpi-top">
          <h4>Hiring Ratio</h4>

          <div className="icon-box purple">
            <FaChartPie />
          </div>
        </div>

        <h2>0.74%</h2>

        <p>Engineers / Headcount</p>

      </div>

      <div className="engineers-kpi-card highlight">

        <div className="kpi-top">
          <h4>Predicted Engineers (2027)</h4>

          <div className="icon-box light-green">
            <FaArrowTrendUp />
          </div>
        </div>

        <h2>38</h2>

        <p>Forecast</p>

      </div>

      <div className="engineers-kpi-card">

        <div className="kpi-top">
          <h4>Headcount Growth</h4>

          <div className="icon-box blue">
            <FaChartLine />
          </div>
        </div>

        <h2>45.71%</h2>

        <p>Overall Growth</p>

      </div>

    </div>
  );
};

export default EngineersKPI;