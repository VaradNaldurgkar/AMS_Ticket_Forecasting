import React, { useEffect, useState } from "react";
import "../../css/HealthSummary.css";

const HealthSummary = () => {
  const [kpis, setKpis] = useState(null);
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/prediction/actual-vs-predicted")
      .then((res) => res.json())
      .then((resData) => {
        setKpis(resData.kpis);
        setData(resData.data);
      })
      .catch((err) => console.error("API Error:", err));
  }, []);

  if (!kpis || data.length === 0) {
    return <div className="summary-container">Loading...</div>;
  }

  // 🔹 Compute derived metrics
  const errors = data.slice(0, 3).map(d => d.error); // Jan–Mar
  const avgError = Math.round(errors.reduce((a, b) => a + b, 0) / errors.length);

  const deviations = data.map(d => ({
    month: d.month,
    deviation: ((d.error / d.actual) * 100)
  }));

  const bestMonth = deviations.reduce((min, curr) =>
    curr.deviation < min.deviation ? curr : min
  );

  const worstMonth = deviations.reduce((max, curr) =>
    curr.deviation > max.deviation ? curr : max
  );

  const totalForecast = data
    .slice(0, 3)
    .reduce((sum, d) => sum + d.predicted, 0);

  return (
    <div className="summary-container">

      {/* Accuracy */}
      <div className="summary-card">
        <h4>Forecast Accuracy</h4>
        <p className="value green">{kpis.accuracy}%</p>
        <span>Excellent</span>
      </div>

      {/* Avg Error */}
      <div className="summary-card">
        <h4>Avg Error (3M)</h4>
        <p className="value">{avgError}</p>
        <span>tickets</span>
      </div>

      {/* Worst Month */}
      <div className="summary-card">
        <h4>Worst Month</h4>
        <p className="value red">{worstMonth.month}</p>
        <span>{worstMonth.deviation.toFixed(1)}% deviation</span>
      </div>

      {/* Best Month */}
      <div className="summary-card">
        <h4>Best Month</h4>
        <p className="value green">{bestMonth.month}</p>
        <span>{bestMonth.deviation.toFixed(1)}% deviation</span>
      </div>

      {/* Total Forecast */}
      <div className="summary-card">
        <h4>Total Forecast</h4>
        <p className="value">{totalForecast.toLocaleString()}</p>
        <span>Next 3 months</span>
      </div>

    </div>
  );
};

export default HealthSummary;