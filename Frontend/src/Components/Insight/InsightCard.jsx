import React from "react";
import "../../css/InsightCard.css";

const InsightCard = () => {
  return (
    <div className="insight-card">

      <div className="insight-header">
        <span className="icon">⚠️</span>
        <h4>April Insight</h4>
      </div>

      <h3 className="insight-title">High Deviation Detected</h3>

      <p className="insight-values">
        Predicted: <b>2809</b> | Actual: <b>1306</b>
      </p>

      <div className="insight-section">
        <h5>AI Insight</h5>
        <p>Ticket volume dropped significantly due to system downtime.</p>
      </div>

      <div className="insight-section">
        <h5>Recommendation</h5>
        <p>Retrain model with anomaly handling and update seasonality factors.</p>
      </div>

      <button className="insight-btn">
        View Full Analysis →
      </button>

    </div>
  );
};

export default InsightCard;