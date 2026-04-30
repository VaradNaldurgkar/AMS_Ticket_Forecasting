import React, { useEffect, useState } from "react";
import "../../css/InsightCard.css";

const InsightCard = () => {
  const [aprilData, setAprilData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/prediction/actual-vs-predicted")
      .then(res => res.json())
      .then(data => {
        const april = data.data.find(d => d.month === "Apr 2026");
        setAprilData(april);
      })
      .catch(err => console.error(err));
  }, []);

  if (!aprilData) {
    return <div className="insight-card">Loading insight...</div>;
  }

  const { actual, predicted, error } = aprilData;

  const deviation = ((error / actual) * 100).toFixed(1);
  const isHigh = deviation > 20;

  // 🔥 Simple rule-based AI insight
  const insightText = isHigh
    ? "Ticket volume dropped significantly due to system anomaly or outage."
    : "Model predictions are within acceptable deviation.";

  const recommendation = isHigh
    ? "Retrain model with anomaly handling and update seasonality factors."
    : "Continue monitoring model performance.";

  return (
    <div className="insight-card">

      <div className="insight-header">
        <span className="icon">⚠️</span>
        <h4>April Insight</h4>
      </div>

      <h3 className="insight-title">
        {isHigh ? "High Deviation Detected" : "Normal Behavior"}
      </h3>

      <p className="insight-values">
        Predicted: <b>{predicted}</b> | Actual: <b>{actual}</b>
      </p>

      <div className="insight-section">
        <h5>AI Insight</h5>
        <p>{insightText}</p>
      </div>

      <div className="insight-section">
        <h5>Recommendation</h5>
        <p>{recommendation}</p>
      </div>

      <button className="insight-btn">
        View Full Analysis →
      </button>

    </div>
  );
};

export default InsightCard;