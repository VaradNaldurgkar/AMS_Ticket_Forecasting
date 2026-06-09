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
} from "recharts";

const WorkforceOverview = ({ data }) => {
  return (
    <div className="workforce-card dashboard-card">

      <h2>Workforce Overview</h2>

      <p>
        Projected tickets vs required engineers
      </p>

      <div className="overview-content">

        <div className="insight-box">

          <h4>Key Insight</h4>

          <p>
            Based on current forecasts, you'll need an
            average of{" "}
            <b>
              {Math.round(
                data.reduce(
                  (sum, item) =>
                    sum + item.engineers,
                  0
                ) / data.length
              )} engineers
            </b>{" "}
            to maintain service levels.
          </p>

        </div>

        <div className="chart-area">

          <ResponsiveContainer width="100%" height={320}>

            <LineChart data={data}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="month" />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="tickets"
                stroke="#10b981"
                strokeWidth={3}
              />

              <Line
                type="monotone"
                dataKey="engineers"
                stroke="#2563eb"
                strokeWidth={3}
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

      </div>

    </div>
  );
};

export default WorkforceOverview;