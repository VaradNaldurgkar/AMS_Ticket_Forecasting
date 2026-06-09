import "../../css/KeyInsights.css";
import {
  FaChartLine,
  FaUsers,
  FaPercentage,
  FaCheckCircle,
  FaUserTie
} from "react-icons/fa";

const KeyInsights = () => {
  return (
    <div className="insights-card">

      <h3>Key Insights for Management</h3>

      <div className="insights-grid">

        {/* Headcount Growth */}
        <div className="insight-item">
          <div className="insight-icon green">
            <FaChartLine />
          </div>

          <div className="insight-content">
            <h4>Headcount Growth</h4>
            <p>
              <b>45.71%</b> increase from 2024–2026
            </p>
          </div>
        </div>

        {/* Hiring Trend */}
        <div className="insight-item">
          <div className="insight-icon blue">
            <FaUsers />
          </div>

          <div className="insight-content">
            <h4>Hiring Trend</h4>
            <p>
              Increased from <b>26</b> to <b>38</b>
            </p>
          </div>
        </div>

        {/* Hiring Ratio */}
        <div className="insight-item">
          <div className="insight-icon purple">
            <FaPercentage />
          </div>

          <div className="insight-content">
            <h4>Hiring Ratio</h4>
            <p>
              Stable at <b>0.74%</b>
            </p>
          </div>
        </div>

        {/* Forecast */}
        <div className="insight-item">
          <div className="insight-icon success">
            <FaCheckCircle />
          </div>

          <div className="insight-content">
            <h4>Forecast</h4>
            <p>
              Approximately <b>38 engineers</b> annually
            </p>
          </div>
        </div>

        {/* Business Impact */}
        <div className="insight-item">
          <div className="insight-icon orange">
            <FaUserTie />
          </div>

          <div className="insight-content">
            <h4>Business Impact</h4>
            <p>
              Supports planning, budgeting and resource allocation
            </p>
          </div>
        </div>

      </div>

    </div>
  );
};

export default KeyInsights;