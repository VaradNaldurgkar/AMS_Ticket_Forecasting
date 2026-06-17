import React from "react";
import "../css/EngineerStats.css";

import {
  FaLayerGroup,
  FaChartLine,
  FaTicketAlt,
  FaUsers,
  FaCalendarAlt,
} from "react-icons/fa";

const EngineerStats = ({ data }) => {

  // ======================================================
  // TOTAL TICKETS
  // ======================================================

  const totalTickets = data.reduce(
  (sum, item) => sum + (item.tickets || 0),
  0
);

  // ======================================================
  // AVG ENGINEERS
  // ======================================================

  const avgEngineers =
  data.length > 0
    ? data.reduce(
        (sum, item) =>
          sum + (item.engineers || 0),
        0
      ) / data.length
    : 0;

  // ======================================================
  // PEAK MONTH
  // ======================================================

  const peakMonth = [...data].sort(
    (a, b) => b.engineers - a.engineers
  )[0];

  // ======================================================
  // DOMINANT CATEGORY
  // ======================================================

  const categoryMap = {};

  data.forEach((monthData) => {

    monthData.workloadBreakdown?.forEach(
      (item) => {

        const category =
          item.category;

        if (!categoryMap[category]) {

          categoryMap[category] = 0;

        }

        categoryMap[category] +=
          item.distribution_percentage;

      }
    );

  });

  const dominantCategory =
    Object.entries(categoryMap).sort(
      (a, b) => b[1] - a[1]
    )[0];

  // ======================================================
  // UI
  // ======================================================

  return (

    <div className="stats-grid">

      {/* DOMINANT CATEGORY */}

      <div className="stat-card">

        <div className="stat-icon blue">
          <FaLayerGroup />
        </div>

        <h4>Dominant Category</h4>

        <h2>
          {dominantCategory?.[0]}
        </h2>

        <p>
  {dominantCategory?.[1]
    ? dominantCategory[1].toFixed(1)
    : 0}
  % workload share
</p>

      </div>

      {/* PRODUCTIVE CAPACITY */}

      <div className="stat-card">

        <div className="stat-icon green">
          <FaChartLine />
        </div>

        <h4>Productive Capacity</h4>

        <h2>7,400</h2>

        <p>
          mins / engineer / month
        </p>

      </div>

      {/* TOTAL FORECASTED TICKETS */}

      <div className="stat-card">

        <div className="stat-icon purple">
          <FaTicketAlt />
        </div>

        <h4>Total Forecasted Tickets</h4>

        <h2>
          {totalTickets.toLocaleString()}
        </h2>

        <p>Next 3 months</p>

      </div>

      {/* AVG FTE */}

      <div className="stat-card">

        <div className="stat-icon orange">
          <FaUsers />
        </div>

        <h4>Avg FTE Required</h4>

        <h2>
          {Math.round(avgEngineers)}
        </h2>

        <p>Engineers</p>

      </div>

      {/* PEAK MONTH */}

      <div className="stat-card">

        <div className="stat-icon pink">
          <FaCalendarAlt />
        </div>

        <h4>Peak Month</h4>

        <h2>
          {peakMonth?.month}
        </h2>

        <p>
          {peakMonth?.engineers} Engineers
        </p>

      </div>

    </div>

  );

};

export default EngineerStats;