import React from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine,
} from "recharts";
import "../css/TrendLineChart.css";

const data = [
  { week: "Week 1", incidents: 280 },
  { week: "Week 2", incidents: 310 },
  { week: "Week 3", incidents: 295 },
  { week: "Week 4", incidents: 340 },
  { week: "Week 5", incidents: 315 },
  { week: "Week 6", incidents: 362 },
];

const avg = Math.round(data.reduce((s, d) => s + d.incidents, 0) / data.length);

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div className="line-tooltip">
        <p className="line-tooltip__week">{label}</p>
        <p className="line-tooltip__val">{payload[0].value} incidents</p>
      </div>
    );
  }
  return null;
};

const TrendLineChart = () => (
  <div className="line-chart-card">
    <div className="line-chart-card__header">
      <div>
        <h3 className="line-chart-card__title">Volume Trend</h3>
        <p className="line-chart-card__sub">Weekly incident count</p>
      </div>
      <div className="line-chart-card__chips">
        <span className="chip chip--up">↑ BitLocker</span>
        <span className="chip chip--up">↑ MS Office</span>
        <span className="chip chip--dn">↓ Zscalar</span>
        <span className="chip chip--dn">↓ Macbook</span>
      </div>
    </div>
    <ResponsiveContainer width="100%" height={160}>
      <LineChart data={data} margin={{ top: 8, right: 10, left: -20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="4 4" stroke="#f0f4f3" />
        <XAxis dataKey="week" tick={{ fontSize: 11, fill: "#9ca3af" }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fontSize: 11, fill: "#9ca3af" }} axisLine={false} tickLine={false} domain={["auto", "auto"]} />
        <Tooltip content={<CustomTooltip />} />
        <ReferenceLine
          y={avg} stroke="#d1d5db" strokeDasharray="5 5"
          label={{ value: `Avg ${avg}`, position: "insideTopRight", fontSize: 10, fill: "#9ca3af" }}
        />
        <Line
          type="monotone" dataKey="incidents"
          stroke="#1d9e75" strokeWidth={2.5}
          dot={{ r: 4, fill: "#1d9e75", strokeWidth: 0 }}
          activeDot={{ r: 6, fill: "#0f6e56" }}
        />
      </LineChart>
    </ResponsiveContainer>
  </div>
);

export default TrendLineChart;