import React from "react";
import "../css/WorkforceOverview.css";

import {
  ResponsiveContainer,
  LineChart,
 Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

const WorkforceOverview = ({ data }) => {

  const avgIncrease = (
    data.reduce(
      (sum, item) =>
        sum + (item.productivityIncreaseNeeded || 0),
      0
    ) / data.length
  ).toFixed(1);

  return (
    <div className="workforce-card dashboard-card">

      <h2>Workforce Overview</h2>

      <p>
        Productivity requirement vs current team capability
      </p>

      <div className="overview-content">

        <div className="insight-box">

          <h4>Key Insight</h4>

          <p>
            Across Jan–Aug 2026, productivity must increase by an average of{" "}
            <b>{avgIncrease}%</b> to meet workload demand.
          </p>

        </div>

        <div className="chart-area">

          <ResponsiveContainer width="100%" height={360}>

            <LineChart data={data}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis
                dataKey="month"
                angle={-25}
                textAnchor="end"
                height={70}
              />

              <YAxis />

              <Tooltip />

              <Legend />

              <Line
                type="monotone"
                dataKey="avgProductivity"
                name="Current Productivity"
                stroke="#10b981"
                strokeWidth={3}
                dot={{ r: 4 }}
              />

              <Line
                type="monotone"
                dataKey="requiredTicketsPerEngineer"
                name="Required Productivity"
                stroke="#2563eb"
                strokeWidth={3}
                dot={{ r: 4 }}
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

      </div>

    </div>
  );
};

export default WorkforceOverview;