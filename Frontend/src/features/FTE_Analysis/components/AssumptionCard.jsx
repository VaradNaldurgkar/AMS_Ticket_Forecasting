import React from "react";

import "../css/AssumptionCard.css";

const AssumptionCard = () => {

  return (

    <div className="assumption-card dashboard-card">

      {/* HEADER */}

      <div className="assumption-header">

        <h2>
          Assumptions & Forecast Logic
        </h2>

        <p>
          Workforce planning assumptions used for FTE forecasting
        </p>

      </div>

      {/* METRICS */}

      <div className="assumption-grid">

        <div className="assumption-metric">

          <span className="metric-label">
            Forecast Model
          </span>

          <h3>
            XGBoost Regression
          </h3>

          <p>
            Time-series ticket forecasting
          </p>

        </div>

        <div className="assumption-metric">

          <span className="metric-label">
            Productive Capacity
          </span>

          <h3>
            7,400
          </h3>

          <p>
            mins / engineer / month
          </p>

        </div>

        <div className="assumption-metric">

          <span className="metric-label">
            SLA Dataset
          </span>

          <h3>
            Feb 2026
          </h3>

          <p>
            Historical resolution data
          </p>

        </div>

        <div className="assumption-metric">

          <span className="metric-label">
            Resolution Logic
          </span>

          <h3>
            Dynamic
          </h3>

          <p>
            Category & priority based
          </p>

        </div>

      </div>

      {/* FORMULA */}

      <div className="formula-section">

        <h4>
          Workforce Formula
        </h4>

        <div className="formula-box">

          FTE = Σ(Category Tickets × Avg Resolution Time)
          ÷ Productive Capacity

        </div>

      </div>

      {/* LOGIC */}

      <div className="logic-box">

        Future category workload distribution is derived
        from historical SLA patterns observed in the
        Feb 2026 dataset.

      </div>

    </div>

  );

};

export default AssumptionCard;