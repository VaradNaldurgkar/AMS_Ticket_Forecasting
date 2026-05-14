import React, { useState } from "react";

import "../css/StatusTable.css";

const StatusTable = ({ data }) => {

  const [sortKey, setSortKey] = useState("incident_count");

  const [sortDir, setSortDir] = useState("desc");

  if (!data) return null;

  // ====================================================
  // SORTING
  // ====================================================

  const sorted = [...data].sort((a, b) => {

    if (sortKey === "incident_count") {

      return sortDir === "desc"

        ? b.incident_count - a.incident_count

        : a.incident_count - b.incident_count;
    }

    if (sortKey === "incident_type") {

      return sortDir === "desc"

        ? b.incident_type.localeCompare(a.incident_type)

        : a.incident_type.localeCompare(b.incident_type);
    }

    return 0;
  });

  // ====================================================
  // TOGGLE SORT
  // ====================================================

  const toggleSort = (key) => {

    if (sortKey === key) {

      setSortDir((d) =>
        d === "desc" ? "asc" : "desc"
      );

    } else {

      setSortKey(key);

      setSortDir("desc");
    }
  };

  const chevron = (key) =>

    sortKey === key

      ? sortDir === "desc"

        ? " ↓"

        : " ↑"

      : "";

  // ====================================================
  // JSX
  // ====================================================

  return (

    <div className="status-table-card">

      <div className="status-table-card__header">

        <h3 className="status-table-card__title">

          Resolution Metrics

        </h3>

        <span className="status-table-card__count">

          {data.length} types

        </span>

      </div>

      <div className="status-table-wrapper">

        <table className="status-table">

          <thead>

            <tr>

              <th
                className="sortable"
                onClick={() =>
                  toggleSort("incident_type")
                }
              >

                Incident Type
                {chevron("incident_type")}

              </th>

              <th
                className="sortable"
                onClick={() =>
                  toggleSort("incident_count")
                }
              >

                Tickets
                {chevron("incident_count")}

              </th>

              <th>
                Avg Resolution
              </th>

              <th>
                Median Resolution
              </th>

            </tr>

          </thead>

          <tbody>

            {sorted.map((row, i) => (

              <tr
                key={i}
                className="status-table__row"
              >

                <td className="status-table__name">

                  {row.incident_type}

                </td>

                <td className="status-table__count">

                  {row.incident_count}

                </td>

                <td>

                  {row.avg_resolution_hours} hrs

                </td>

                <td>

                  {row.median_resolution_hours} hrs

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
};

export default StatusTable;