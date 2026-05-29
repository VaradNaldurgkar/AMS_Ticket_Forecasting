import React from "react";
import "../css/FteSummary.css";

const FteSummary = ({ data }) => {

  const total = data.reduce(
    (sum, item) => sum + item.engineers,
    0
  );

  return (
    <div className="fte-summary dashboard-card">

      <h2>
        FTE Summary
        <span>(Next 3 Months)</span>
      </h2>

      <div className="donut-chart">
        <div className="donut-center">
          <h1>{total}</h1>
          <p>Engineer Months</p>
        </div>
      </div>

      <div className="summary-list">

        {data.map((item, index) => (
          <div className="summary-item" key={index}>

            <div className="left">

              <span className={`dot dot-${index}`}></span>

              <span>{item.month}</span>

            </div>

            <div className="right">
              {item.engineers}
            </div>

          </div>
        ))}

      </div>

    </div>
  );
};

export default FteSummary;