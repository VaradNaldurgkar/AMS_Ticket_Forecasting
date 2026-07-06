import React from "react";

import "../css/CategoryBreakdownModal.css";

const CategoryBreakdownModal = ({
  isOpen,
  month,
  workforceData,
  onClose
}) => {

  if (!isOpen) {
    return null;
  }

  const riskLevel =
    workforceData?.productivityIncreaseNeeded > 15
      ? "HIGH"
      : workforceData?.productivityIncreaseNeeded > 5
      ? "MEDIUM"
      : "LOW";

  const avgProd =
    workforceData?.avgProductivity ?? 0;

  const requiredProd =
    workforceData?.requiredTicketsPerEngineer ?? 0;

  const tickets =
    workforceData?.tickets ?? 0;

  const engineers =
    workforceData?.availableEngineers ?? 0;

  const productivityGap =
    workforceData?.productivityGap ?? 0;

  // DEBUG LOGS
  console.log("MODAL workforceData:", workforceData);
  console.log("MODAL productivityGap:", productivityGap);

  return (
    <div className="modal-overlay">

      <div className="modal-container">

        <div className="modal-header">

          <div>
            <h2>Workforce Analysis - {month}</h2>
            <p>Forecast vs Current Workforce Capacity</p>
          </div>

          <button
            className="close-btn"
            onClick={onClose}
          >
            ✕
          </button>

        </div>

        <div className="modal-body">

          {/* Executive Summary */}
          <div className="executive-grid">

            <div className="metric-card">
              <span>Predicted Tickets</span>
              <strong>
                {tickets.toLocaleString()}
              </strong>
            </div>

            <div className="metric-card">
              <span>Current Capacity</span>
              <strong>
                {workforceData?.monthlyCapacity?.toLocaleString()}
              </strong>
            </div>

            <div className="metric-card">
              <span>Ticket Gap</span>
              <strong>
                {workforceData?.ticketGap?.toLocaleString()}
              </strong>
            </div>

            <div className="metric-card">
              <span>Required Productivity / Engineer</span>
              <strong>
                {requiredProd}
              </strong>
            </div>

          </div>

          {/* Workforce Metrics */}
          <div className="analysis-section">

            <h3>Workforce Metrics</h3>

            <table className="metrics-table">
              <thead>
                <tr>
                  <th>Metric</th>
                  <th>Value</th>
                  <th>Formula</th>
                  <th>Explanation</th>
                </tr>
              </thead>

              <tbody>
                <tr>
                  <td>Available Engineers</td>
                  <td>{engineers}</td>
                  <td>Current Team</td>
                  <td>Engineers dedicated to ticket resolution</td>
                </tr>

                <tr>
                  <td>Avg Productivity</td>
                  <td>{avgProd}</td>
                  <td>(77 + 115 + 97 + 117 + 85) / 5 = {avgProd}</td>
                  <td>
                    Average productivity calculated using Jan–May historical
                    resolved tickets per engineer.
                  </td>
                </tr>

                <tr>
                  <td>Monthly Capacity</td>
                  <td>{workforceData?.monthlyCapacity}</td>
                  <td>
                    {engineers} × {avgProd} = {workforceData?.monthlyCapacity}
                  </td>
                  <td>Total team handling capacity</td>
                </tr>

                <tr>
                  <td>Required Tickets / Engineer</td>
                  <td>{requiredProd}</td>
                  <td>
                    {tickets} / {engineers} = {requiredProd}
                  </td>
                  <td>Expected workload per engineer</td>
                </tr>

                <tr>
                  <td>Productivity Gap</td>
                  <td>{productivityGap}</td>
                  <td>
                    {requiredProd} - {avgProd} = {productivityGap}
                  </td>
                  <td>Extra tickets each engineer must resolve</td>
                </tr>

                <tr>
                  <td>Productivity Increase Needed</td>
                  <td>{workforceData?.productivityIncreaseNeeded}%</td>
                  <td>
                    (({requiredProd} - {avgProd}) / {avgProd}) × 100
                  </td>
                  <td>Improvement needed with same team</td>
                </tr>
              </tbody>
            </table>

          </div>

          {/* Recommendations */}
          <div className="analysis-section">

            <h3>Recommendations</h3>

            <table className="recommendation-table">
              <thead>
                <tr>
                  <th>Recommendation</th>
                  <th>Action Plan</th>
                </tr>
              </thead>

              <tbody>
                <tr>
                  <td>Productivity Strategy</td>
                  <td>
                    Improve productivity by{" "}
                    {workforceData?.productivityIncreaseNeeded}% through
                    automation, workflow optimization, and faster ticket handling.
                  </td>
                </tr>

                <tr>
                  <td>Capacity Strategy</td>
                  <td>
                    Each engineer should target resolving{" "}
                    {requiredProd} tickets in {month}.
                  </td>
                </tr>
              </tbody>
            </table>

          </div>

          {/* Risk */}
          <div className="analysis-section">

            <h3>Risk Assessment</h3>

            <div className="risk-card">
              <div className={`risk-badge ${riskLevel.toLowerCase()}`}>
                {riskLevel}
              </div>

              <p>
                Current productivity levels may not fully meet projected workload demand.
              </p>
            </div>

          </div>

          {/* Insights */}
          <div className="analysis-section">

            <h3>Key Insights</h3>

            <div className="insights-list">
              <div className="insight-row">
                Current team capacity is{" "}
                <strong>
                  {workforceData?.monthlyCapacity?.toLocaleString()}
                </strong>{" "}
                tickets/month.
              </div>

              <div className="insight-row">
                Predicted demand requires{" "}
                <strong>
                  {requiredProd}
                </strong>{" "}
                tickets per engineer.
              </div>

              <div className="insight-row">
                Productivity gap per engineer:{" "}
                <strong>
                  {productivityGap}
                </strong>{" "}
                tickets.
              </div>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
};

export default CategoryBreakdownModal;