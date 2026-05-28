import React from "react";

import "../css/FteAnalysisTable.css";

const FteAnalysisTable = ({ data }) => {

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

                  {/* MONTH */}

                  <td>
                    {item.month}
                  </td>

                  {/* TICKETS */}

                  <td>
                    {item.tickets.toLocaleString()}
                  </td>

                  {/* TOTAL EFFORT */}

                  <td>
                    {Math.round(
                      item.totalEffort
                    ).toLocaleString()}
                  </td>

                  {/* FTE */}

                  <td>
                    {item.fte}
                  </td>

                  {/* ENGINEERS */}

                  <td>
                    {item.engineers}
                  </td>

                  {/* CAPACITY */}

                  <td>
                    {item.capacity.toLocaleString()}
                  </td>

                  {/* DOMINANT PRIORITY */}

                  <td>

                    <span className="priority-badge">

                      {
                        priorityInsight
                          .dominantPriority
                      }

                    </span>

                  </td>

                  {/* CONTRIBUTION */}

                  <td>

                    <span className="contribution-text">

                      {
                        priorityInsight
                          .contribution
                      }

                    </span>

                  </td>

                  {/* UTILIZATION */}

                  <td>

                    <div className="utilization-cell">

                      <span>
                        {item.utilization}%
                      </span>

                      <div className="progress-bar">

                        <div
                          className="progress-fill"
                          style={{

                            width:
                              `${item.utilization}%`

                          }}
                        ></div>

                      </div>

                    </div>

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