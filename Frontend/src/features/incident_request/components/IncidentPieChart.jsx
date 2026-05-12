import React, { useState } from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import "../css/IncidentPieChart.css";

const data = [
  { name: "BitLocker Issue", value: 63, color: "#1d9e75" },
  { name: "PKI Certificates", value: 60, color: "#534AB7" },
  { name: "Authentication", value: 60, color: "#D85A30" },
  { name: "Wi-Fi Issue", value: 55, color: "#378ADD" },
  { name: "Outlook Issue", value: 46, color: "#BA7517" },
  { name: "Others", value: 1469, color: "#b4b2a9" },
];

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    const d = payload[0].payload;
    return (
      <div className="pie-tooltip">
        <span className="pie-tooltip__dot" style={{ background: d.color }} />
        <span className="pie-tooltip__name">{d.name}</span>
        <span className="pie-tooltip__value">{d.value}</span>
      </div>
    );
  }
  return null;
};

const IncidentPieChart = () => {
  const [activeIndex, setActiveIndex] = useState(null);

  return (
    <div className="pie-chart-card">
      <div className="pie-chart-card__header">
        <h3 className="pie-chart-card__title">Bifurcation by Incident Type</h3>
        <span className="pie-chart-card__badge">Top 5 + Others</span>
      </div>
      <div className="pie-chart-card__body">
        <div className="pie-chart-card__chart">
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={data}
                cx="50%" cy="50%"
                innerRadius={55} outerRadius={90}
                paddingAngle={2} dataKey="value"
                onMouseEnter={(_, i) => setActiveIndex(i)}
                onMouseLeave={() => setActiveIndex(null)}
              >
                {data.map((entry, index) => (
                  <Cell
                    key={index}
                    fill={entry.color}
                    opacity={activeIndex === null || activeIndex === index ? 1 : 0.45}
                    stroke="none"
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
          <div className="pie-chart-card__center-label">
            <span className="pie-chart-card__total">1,842</span>
            <span className="pie-chart-card__total-sub">Total</span>
          </div>
        </div>
        <div className="pie-chart-card__legend">
          {data.map((entry, i) => (
            <div
              className={`legend-row ${activeIndex === i ? "legend-row--active" : ""}`}
              key={i}
              onMouseEnter={() => setActiveIndex(i)}
              onMouseLeave={() => setActiveIndex(null)}
            >
              <span className="legend-row__dot" style={{ background: entry.color }} />
              <span className="legend-row__name">{entry.name}</span>
              <span className="legend-row__count">{entry.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default IncidentPieChart;