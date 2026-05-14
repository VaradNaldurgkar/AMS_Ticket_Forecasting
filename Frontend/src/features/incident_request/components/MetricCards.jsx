import React from "react";
import "../css/MetricCards.css";

const MetricCards = ({ data }) => {

  if (!data) return null;

  const metrics = [

    {
      label: "Total Incidents",

      value: data.total_incidents?.toLocaleString(),

      sub: "All logged incidents",
    },

    {
      label: "Top Incident Type",

      value: data.top_incident,

      sub: `${data.top_incident_count} tickets raised`,
    },

    {
      label: "Total Categories",

      value: data.total_categories,

      sub: "Distinct incident types",
    },
  ];

  return (

    <div className="metric-cards-grid">

      {metrics.map((m, i) => (

        <div className="metric-card" key={i}>

          <div className="metric-card__label">
            {m.label}
          </div>

          <div className="metric-card__value">
            {m.value}
          </div>

          <div className="metric-card__sub">
            {m.sub}
          </div>

        </div>

      ))}

    </div>
  );
};

export default MetricCards;