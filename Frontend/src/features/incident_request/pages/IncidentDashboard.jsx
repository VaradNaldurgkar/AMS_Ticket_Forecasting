import React, { useEffect, useState } from "react";
import axios from "axios";

import MetricCards from "../components/MetricCards";
import IncidentBarChart from "../components/IncidentBarChart";
import StatusTable from "../components/StatusTable";

import "../css/IncidentDashboard.css";

const IncidentDashboard = () => {

  // ======================================================
  // STATE
  // ======================================================

  const [dashboardData, setDashboardData] = useState(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  // ======================================================
  // API CALL
  // ======================================================

  useEffect(() => {

    const fetchDashboardData = async () => {

      try {

        const response = await axios.get(
          "http://127.0.0.1:8000/api/incident-dashboard"
        );

        setDashboardData(response.data);

      } catch (err) {

        console.error(err);

        setError("Failed to load dashboard data");

      } finally {

        setLoading(false);
      }
    };

    fetchDashboardData();

  }, []);

  // ======================================================
  // LOADING
  // ======================================================

  if (loading) {

    return (
      <div className="incident-dashboard">

        <h2>Loading dashboard...</h2>

      </div>
    );
  }

  // ======================================================
  // ERROR
  // ======================================================

  if (error) {

    return (
      <div className="incident-dashboard">

        <h2>{error}</h2>

      </div>
    );
  }

  // ======================================================
  // API DATA
  // ======================================================

  const summaryCards = dashboardData?.summary_cards;

  const chartData = dashboardData?.chart_data;

  // ======================================================
  // REMOVE GENERAL / UNCATEGORIZED
  // FROM CHART ONLY
  // ======================================================

  const filteredChartData = chartData?.filter(

    (item) =>

      item.Incident_Type !==
      "General / Uncategorized"

  );

  const tableData = dashboardData?.table_data;

  // ======================================================
  // JSX
  // ======================================================

  return (

    <div className="incident-dashboard">

      {/* ================================================= */}
      {/* HEADER */}
      {/* ================================================= */}

      <div className="incident-dashboard__header">

        <div>

          <h2 className="incident-dashboard__title">

            Incident Request Bifurcation

          </h2>

          <p className="incident-dashboard__sub">

            Overview of incident requests by category and resolution metrics

          </p>

        </div>

      </div>

      {/* ================================================= */}
      {/* METRIC CARDS */}
      {/* ================================================= */}

      <MetricCards data={summaryCards} />

      {/* ================================================= */}
      {/* CHARTS + TABLE */}
      {/* ================================================= */}

      <div className="incident-dashboard__row-2">

        {/* ============================================= */}
        {/* BAR CHART */}
        {/* ============================================= */}

        <IncidentBarChart
          data={filteredChartData}
        />

        {/* ============================================= */}
        {/* TABLE */}
        {/* ============================================= */}

        <StatusTable
          data={tableData}
        />

      </div>

    </div>
  );
};

export default IncidentDashboard;