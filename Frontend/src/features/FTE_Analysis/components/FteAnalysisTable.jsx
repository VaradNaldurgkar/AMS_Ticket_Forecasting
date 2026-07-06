import React from "react";
import "../css/FteAnalysisTable.css";

const FteAnalysisTable = ({
  data,
  onViewBreakdown
}) => {

  return (

    <div className="fte-table dashboard-card">

      <h2>
        Workforce Capacity Analysis
      </h2>

      <p>
        Month-wise engineer productivity and workload planning
      </p>

      <table>

        <thead>
          <tr>
            <th>Month</th>
            <th>Predicted Tickets</th>
            <th>Available Engineers</th>
            <th>Avg Productivity</th>
            <th>Current Capacity</th>
            <th>Required Tickets / Engineer</th>
            <th>Productivity Gap</th>
            <th>Increase Needed</th>
            <th>Details</th>
          </tr>
        </thead>

        <tbody>

          {data.map((item, index) => (

            <tr key={index}>

              <td>
                {item.month}
              </td>

              <td>
                {(item.tickets ?? 0).toLocaleString()}
              </td>

              <td>
                {item.availableEngineers ?? "-"}
              </td>

              <td>
                {item.avgProductivity ?? "-"}
              </td>

              <td>
                {(item.monthlyCapacity ?? 0).toLocaleString()}
              </td>

              <td>
                {item.requiredTicketsPerEngineer ?? "-"}
              </td>

              <td>
                {(item.productivityGap ?? 0) > 0
                  ? `+${item.productivityGap}`
                  : item.productivityGap}
              </td>

              <td>
                {item.productivityIncreaseNeeded ?? 0}%
              </td>

              <td>
                <button
                  className="info-btn"
                  onClick={() =>
                    onViewBreakdown(item.month)
                  }
                  title="View Workforce Analysis"
                >
                  i
                </button>
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );

};

export default FteAnalysisTable;