import React from "react";
import "../css/MetricCards.css";

const metrics = [
  {
    label: "Total Incidents",
    value: "1,842",
    sub: "All logged incidents",
  },
  {
    label: "Top Incident Type",
    value: "BitLocker Issue",
    sub: "63 tickets raised",
  },
  {
    label: "Total Categories",
    value: "24",
    sub: "Distinct incident types",
  },
];

const MetricCards = () => (
  <div className="metric-cards-grid">
    {metrics.map((m, i) => (
      <div className="metric-card" key={i}>
        <div className="metric-card__label">{m.label}</div>
        <div className="metric-card__value">{m.value}</div>
        <div className="metric-card__sub">{m.sub}</div>
      </div>
    ))}
  </div>
);

export default MetricCards;