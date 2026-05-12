import React from "react";
import MetricCards from "../components/MetricCards";
import IncidentBarChart from "../components/IncidentBarChart";
import StatusTable from "../components/StatusTable";
import "../css/IncidentDashboard.css";

const IncidentDashboard = () => {
  return (
    <div className="incident-dashboard">
      <div className="incident-dashboard__header">
        <div>
          <h2 className="incident-dashboard__title">Incident Request Bifurcation</h2>
          <p className="incident-dashboard__sub">Overview of incident requests by category and status</p>
        </div>
        
      </div>
      <MetricCards />
      <div className="incident-dashboard__row-2">
        <IncidentBarChart />
        <StatusTable />
      </div>
    </div>
  );
};

export default IncidentDashboard;