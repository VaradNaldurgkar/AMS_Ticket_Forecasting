import React, { useState } from "react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

import "../css/IncidentBarChart.css";

const CustomTooltip = ({ active, payload, label }) => {

  if (active && payload?.length) {

    return (

      <div className="bar-tooltip">

        <p className="bar-tooltip__label">
          {label}
        </p>

        <p className="bar-tooltip__value">
          {payload[0].value} tickets
        </p>

      </div>
    );
  }

  return null;
};

const IncidentBarChart = ({ data }) => {

  const [activeBar, setActiveBar] = useState(null);

  if (!data) return null;

  return (

    <div className="bar-chart-card">

      <div className="bar-chart-card__header">

        <h3 className="bar-chart-card__title">

          Top Incident Requests

        </h3>

        <span className="bar-chart-card__sub">

          Top 5 by volume

        </span>

      </div>

      <ResponsiveContainer width="100%" height={280}>

        <BarChart
          layout="vertical"
          data={data}
          margin={{
            top: 0,
            right: 40,
            left: 10,
            bottom: 0,
          }}
          onMouseLeave={() => setActiveBar(null)}
        >

          <CartesianGrid
            strokeDasharray="4 4"
            horizontal={false}
            stroke="#f0f0f0"
          />

          <XAxis
            type="number"
            tick={{
              fontSize: 11,
              fill: "#9ca3af"
            }}
            axisLine={false}
            tickLine={false}
          />

          <YAxis
            dataKey="name"
            type="category"
            tick={{
              fontSize: 15,
              fill: "#4b5563"
            }}
            axisLine={false}
            tickLine={false}
            width={130}
          />

          <Tooltip
            content={<CustomTooltip />}
            cursor={{ fill: "#f9fafb" }}
          />

          <Bar
            dataKey="tickets"
            radius={[0, 6, 6, 0]}
            maxBarSize={18}
            onMouseEnter={(_, i) => setActiveBar(i)}
          >

            {data.map((_, i) => (

              <Cell
                key={i}
                fill={
                  activeBar === i
                    ? "#1d9e75"
                    : "#9FE1CB"
                }
              />

            ))}

          </Bar>

        </BarChart>

      </ResponsiveContainer>

    </div>
  );
};

export default IncidentBarChart;