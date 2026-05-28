import React from "react";
import "../css/AssumptionCard.css";

const AssumptionCard = () => {
  return (
    <div className="assumption-card dashboard-card">

      <h2>Assumptions Used</h2>

      <div className="assumption-item">
        <h4>Avg Resolution Time</h4>
        <p>110 minutes / ticket</p>
      </div>

      <div className="assumption-item">
        <h4>Productive Capacity</h4>
        <p>7,400 minutes / engineer / month</p>
      </div>

      <div className="assumption-item">
        <h4>Formula</h4>

        <div className="formula-box">
          FTE = (Predicted Tickets × Avg Resolution Time)
          ÷ Productive Capacity
        </div>
      </div>

      <div className="warning-box">
        These assumptions can be updated in settings to
        recalculate results.
      </div>

    </div>
  );
};

export default AssumptionCard;