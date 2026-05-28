import React from "react";

import "../css/CategoryBreakdownTable.css";

const PRODUCTIVE_MINUTES = 7400;

const CategoryBreakdownTable = ({ data }) => {

  return (

    <div className="category-breakdown dashboard-card">

      <div className="breakdown-header">

        <h2>
          Category Workforce Breakdown
        </h2>

        <p>
          Engineer allocation by category and priority
        </p>

      </div>

      {data.map((monthData, monthIndex) => (

        <div
          key={monthIndex}
          className="month-breakdown"
        >

          <div className="month-title">

            {monthData.month}

          </div>

          <div className="table-wrapper">

            <table>

              <thead>

                <tr>

                  <th>Category</th>

                  <th>Priority</th>

                  <th>
                    Estimated Tickets
                  </th>

                  <th>
                    Avg Resolution Time
                  </th>

                  <th>
                    Total Effort
                  </th>

                  <th>
                    Engineers Required
                  </th>

                </tr>

              </thead>

              <tbody>

                {monthData.workloadBreakdown?.map(
                  (item, index) => {

                    const engineersRequired =
                      Math.ceil(
                        item.total_effort /
                        PRODUCTIVE_MINUTES
                      );

                    return (

                      <tr key={index}>

                        <td>
                          {item.category}
                        </td>

                        <td>

                          <span
                            className={`priority-badge priority-${item.priority}`}
                          >

                            P{item.priority}

                          </span>

                        </td>

                        <td>
                          {item.estimated_tickets}
                        </td>

                        <td>
                          {item.avg_resolution_time} mins
                        </td>

                        <td>

                          {Math.round(
                            item.total_effort
                          ).toLocaleString()}

                        </td>

                        <td>

                          <div className="engineer-pill">

                            {engineersRequired}
                            Engineers

                          </div>

                        </td>

                      </tr>

                    );

                  }
                )}

              </tbody>

            </table>

          </div>

        </div>

      ))}

    </div>

  );

};

export default CategoryBreakdownTable;