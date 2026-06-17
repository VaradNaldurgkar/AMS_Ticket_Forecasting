import React from "react";

import "../css/FteAnalysisTable.css";

const FteAnalysisTable = ({
  data,
  onViewBreakdown
}) => {

  // ======================================================
  // GET DOMINANT PRIORITY
  // ======================================================

  const getPriorityInsight = (
    prioritySummary,
    totalEffort
  ) => {

    if (!prioritySummary) {

      return {
        dominantPriority: "-",
        contribution: "-"
      };

    }

    let maxPriority = "";
    let maxEffort = 0;

    Object.entries(prioritySummary).forEach(
      ([priority, value]) => {

        if (value.effort > maxEffort) {

          maxEffort = value.effort;

          maxPriority = priority;

        }

      }
    );

    const contribution = (
      (maxEffort / totalEffort) * 100
    ).toFixed(1);

    return {

      dominantPriority:
        `P${maxPriority}`,

      contribution:
        `${contribution}%`

    };

  };

  return (

    <div className="fte-table dashboard-card">

      <h2>
        FTE Capacity Analysis
      </h2>

      <p>
        Detailed month-wise workforce breakdown
      </p>

      <table>

        <thead>

          <tr>

            <th>Month</th>

            <th>
              Predicted Tickets
            </th>

            <th>
              Total Effort
            </th>

            <th>
              FTE Required
            </th>

            <th>
              Engineers Needed
            </th>

            <th>
              Capacity Available
            </th>

            <th>
              Dominant Priority
            </th>

            <th>
              Priority Contribution
            </th>

            <th>
              Utilization
            </th>

            <th>
              Details
            </th>

          </tr>

        </thead>

        <tbody>

          {data.map(
            (item, index) => {

              const priorityInsight =
                getPriorityInsight(

                  item.prioritySummary,

                  item.totalEffort

                );

              return (

                <tr key={index}>

                  <td>
                    {item.month}
                  </td>

                  <td>
  {(item.tickets ?? 0).toLocaleString()}
</td>

                  <td>
  {Math.round(
    item.totalEffort ?? 0
  ).toLocaleString()}
</td>

                  <td>
                    {item.fte}
                  </td>

                  <td>
                    {item.engineers}
                  </td>

                  <td>
  {(item.capacity ?? 0).toLocaleString()}
</td>

                  <td>

                    <span className="priority-badge">

                      {
                        priorityInsight
                          .dominantPriority
                      }

                    </span>

                  </td>

                  <td>

                    <span className="contribution-text">

                      {
                        priorityInsight
                          .contribution
                      }

                    </span>

                  </td>

                  <td>

                    <div className="utilization-cell">

                      <span>
  {item.utilization ?? 0}%
</span>

                      <div className="progress-bar">

                        <div
                          className="progress-fill"
                          style={{
                            width:
  `${item.utilization ?? 0}%`
                          }}
                        />

                      </div>

                    </div>

                  </td>

                  {/* DETAILS BUTTON */}

                  <td>

                    <button
  className="info-btn"
  onClick={() =>
    onViewBreakdown(item.month)
  }
  title="View Category Breakdown"
>
  i
</button>

                  </td>

                </tr>

              );

            }
          )}

        </tbody>

      </table>

    </div>

  );

};

export default FteAnalysisTable;