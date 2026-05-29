import { useEffect, useState } from "react";

import SummaryCard from "../components/SummaryCard";
import CallCodePieChart from "../components/CallCodePieChart";
import TopServiceRequestsChart from "../components/TopServiceRequestsChart";

import "../css/serviceDashboard.css";

const ServiceDashboard = () => {

  const [dashboardData, setDashboardData] =
    useState(null);

  const [topRequestData, setTopRequestData] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [selectedType, setSelectedType] =
    useState("asset");

  // ======================================================
  // LOAD DASHBOARD BASED ON DROPDOWN
  // ======================================================

  useEffect(() => {

    const loadDashboard = async () => {

      try {

        setLoading(true);

        const dashboardEndpoint =

          selectedType === "asset"

            ? "http://127.0.0.1:8000/api/requisition/asset-dashboard"

            : "http://127.0.0.1:8000/api/requisition/software-dashboard";

        const chartEndpoint =

          selectedType === "asset"

            ? "http://127.0.0.1:8000/api/requisition/asset-breakdown"

            : "http://127.0.0.1:8000/api/requisition/software-breakdown";

        const dashboardResponse =
          await fetch(dashboardEndpoint);

        const chartResponse =
          await fetch(chartEndpoint);

        const dashboardJson =
          await dashboardResponse.json();

        const chartJson =
          await chartResponse.json();

        setDashboardData(
          dashboardJson
        );

        setTopRequestData(
          chartJson
        );

        setLoading(false);

      } catch (err) {

        console.error(err);

        setError(
          "Failed to load dashboard"
        );

        setLoading(false);

      }

    };

    loadDashboard();

  }, [selectedType]);

  // ======================================================
  // LOADING
  // ======================================================

  if (loading) {

    return (

      <div className="service-dashboard">

        <h2>
          Loading Dashboard...
        </h2>

      </div>

    );

  }

  // ======================================================
  // ERROR
  // ======================================================

  if (error) {

    return (

      <div className="service-dashboard">

        <h2>{error}</h2>

      </div>

    );

  }

  // ======================================================
  // SUMMARY CARDS
  // ======================================================

  const summaryData = [

    {
      title: "Total Requests",

      value:
        dashboardData.total_requests.toLocaleString(),

      subtitle:
        selectedType === "asset"
          ? "Asset Requests"
          : "Software Requests",
    },

    {
      title:
        selectedType === "asset"
          ? "Top Requested Asset"
          : "Top Requested Software",

      value:
        dashboardData.top_count.toLocaleString(),

      subtitle:
        dashboardData.top_item,
    },

    {
      title:
        "Total Categories",

      value:
        dashboardData.total_categories.toLocaleString(),

      subtitle:
        "Available Categories",
    },

  ];

  // ======================================================
  // UI
  // ======================================================

  return (

    <div className="service-dashboard">

      {/* HEADER */}

      <div className="dashboard-header">

        <h1>
          Service Ticket Bifurcation
        </h1>

        <p>
          Overview of service request bifurcation
        </p>

        {/* PROFESSIONAL FILTER */}

        <div className="dashboard-filter">

          <span className="filter-label">
            Request Type
          </span>

          <select
            className="filter-select"
            value={selectedType}
            onChange={(e) =>
              setSelectedType(
                e.target.value
              )
            }
          >

            <option value="asset">
              IT Asset Requisition
            </option>

            <option value="software">
              Software Requisition
            </option>

          </select>

        </div>

      </div>

      {/* SUMMARY CARDS */}

      <div className="summary-grid">

        {summaryData.map(
          (card, index) => (

            <SummaryCard
              key={index}
              title={card.title}
              value={card.value}
              subtitle={card.subtitle}
            />

          )
        )}

      </div>

      {/* CHARTS */}

      <div className="top-section">

        <CallCodePieChart
          data={
            dashboardData.pie_chart_data
          }
          selectedType={
            selectedType
          }
        />

        <TopServiceRequestsChart
          data={topRequestData}
          selectedType={
            selectedType
          }
        />

      </div>

    </div>

  );

};

export default ServiceDashboard;