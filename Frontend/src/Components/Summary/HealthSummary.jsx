import React from "react";
import "../../css/HealthSummary.css";

const HealthSummary = () => {
  return (
    <div className="summary-container">

      <div className="summary-card">
        <h4>Forecast Accuracy</h4>
        <p className="value green">94.2%</p>
        <span>Excellent</span>
      </div>

      <div className="summary-card">
        <h4>Avg Error (3M)</h4>
        <p className="value">47</p>
        <span>tickets</span>
      </div>

      <div className="summary-card">
        <h4>Worst Month</h4>
        <p className="value red">March 2026</p>
        <span>4.1% deviation</span>
      </div>

      <div className="summary-card">
        <h4>Best Month</h4>
        <p className="value green">February 2026</p>
        <span>0.4% deviation</span>
      </div>

      <div className="summary-card">
        <h4>Total Forecast</h4>
        <p className="value">8,540</p>
        <span>Next 3 months</span>
      </div>

    </div>
  );
};

export default HealthSummary;