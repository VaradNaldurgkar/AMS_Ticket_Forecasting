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
  // TOTAL FORECASTED TICKETS (ONLY NEXT 3 MONTHS)
  // ======================================================

  const forecastMonths = ["Jun 2026", "Jul 2026", "Aug 2026"];

  const totalForecastTickets = data
    .filter(item => forecastMonths.includes(item.month))
    .reduce(
      (sum, item) => sum + (item.tickets || 0),
      0
    );

  // ======================================================
  // AVG PRODUCTIVITY CAPACITY
  // ======================================================

  const avgProductivity =
    data.length > 0
      ? data[0]?.avgProductivity || 98.2
      : 98.2;

  // ======================================================
  // AVG PRODUCTIVITY INCREASE
  // ======================================================

  const avgProductivityIncrease =
    data.length > 0
      ? (
          data.reduce(
            (sum, item) =>
              sum + (item.productivityIncreaseNeeded || 0),
            0
          ) / data.length
        ).toFixed(1)
      : 0;

  // ======================================================
  // PEAK LOAD MONTH
  // ======================================================

  const peakMonth = [...data].sort(
    (a, b) =>
      (b.productivityIncreaseNeeded || 0) -
      (a.productivityIncreaseNeeded || 0)
  )[0];

  // ======================================================
  // DOMINANT CATEGORY
  // ======================================================

  const categoryMap = {};

  data.forEach((monthData) => {

    monthData.workloadBreakdown?.forEach(
      (item) => {

        const category = item.category;

        if (!categoryMap[category]) {
          categoryMap[category] = 0;
        }

        categoryMap[category] += item.distribution_percentage;

      }
    );

  });

  Object.keys(categoryMap).forEach(category => {
    categoryMap[category] =
      categoryMap[category] / data.length;
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

      {/* AVG PRODUCTIVITY CAPACITY */}
      <div className="stat-card">

        <div className="stat-icon green">
          <FaChartLine />
        </div>

        <h4>Avg Productivity Capacity</h4>

        <h2>{avgProductivity}</h2>

        <p>
          tickets / engineer / month
        </p>

      </div>

      {/* TOTAL FORECASTED TICKETS */}
      <div className="stat-card">

        <div className="stat-icon purple">
          <FaTicketAlt />
        </div>

        <h4>Total Forecasted Tickets</h4>

        <h2>
          {totalForecastTickets.toLocaleString()}
        </h2>

        <p>Next 3 months</p>

      </div>

      {/* AVG PRODUCTIVITY INCREASE */}
      <div className="stat-card">

        <div className="stat-icon orange">
          <FaUsers />
        </div>

        <h4>Avg Productivity Increase</h4>

        <h2>
          {avgProductivityIncrease}%
        </h2>

        <p>Across Jan–Aug 2026</p>

      </div>

      {/* PEAK LOAD MONTH */}
      <div className="stat-card">

        <div className="stat-icon pink">
          <FaCalendarAlt />
        </div>

        <h4>Peak Load Month</h4>

        <h2>
          {peakMonth?.month}
        </h2>

        <p>
          {peakMonth?.productivityIncreaseNeeded}% increase needed
        </p>

      </div>

    </div>

  );

};

export default EngineerStats;