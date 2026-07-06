import React from "react";
import "../css/FteSummary.css";

const FteSummary = ({ data }) => {

  const avgIncrease = (
    data.reduce(
      (sum, item) =>
        sum + (item.productivityIncreaseNeeded || 0),
      0
    ) / data.length
  ).toFixed(1);

  return (
    <div className="fte-summary dashboard-card">

      <h2>
        Productivity Summary
        <span>(Jan–Aug 2026)</span>
      </h2>

      <div className="donut-chart">
        <div className="donut-center">
          <h1>{avgIncrease}%</h1>
          <p>Avg Increase Needed</p>
        </div>
      </div>

      <div className="summary-list">

        {data.map((item, index) => (
          <div className="summary-item" key={index}>

            <div className="left">
              <span className={`dot dot-${index % 8}`}></span>
              <span>{item.month}</span>
            </div>

            <div className="right">
              {item.productivityIncreaseNeeded}%
            </div>

          </div>
        ))}

      </div>

    </div>
  );
};

export default FteSummary;