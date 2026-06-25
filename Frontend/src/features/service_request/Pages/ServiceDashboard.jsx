import { useEffect, useState } from "react";

import SummaryCard from "../components/SummaryCard";
import CallCodePieChart from "../components/CallCodePieChart";
import TopServiceRequestsChart from "../components/TopServiceRequestsChart";

import "../css/serviceDashboard.css";

const ServiceDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [topRequestData, setTopRequestData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [selectedType, setSelectedType] = useState("asset");
  const [selectedYear, setSelectedYear] = useState("all");

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  // ======================================================
  // CLEAR DATE FILTER
  // ======================================================

  const clearDateFilter = () => {
    setStartDate("");
    setEndDate("");
  };

  // ======================================================
  // LOAD DASHBOARD BASED ON FILTERS
  // ======================================================

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        let dashboardEndpoint =
          selectedType === "asset"
            ? `http://127.0.0.1:8000/api/requisition/asset-dashboard?year=${selectedYear}`
            : `http://127.0.0.1:8000/api/requisition/software-dashboard?year=${selectedYear}`;

        let chartEndpoint =
          selectedType === "asset"
            ? `http://127.0.0.1:8000/api/requisition/asset-breakdown?year=${selectedYear}`
            : `http://127.0.0.1:8000/api/requisition/software-breakdown?year=${selectedYear}`;

        if (startDate && endDate) {
          dashboardEndpoint += `&start_date=${startDate}&end_date=${endDate}`;
          chartEndpoint += `&start_date=${startDate}&end_date=${endDate}`;
        }

        const dashboardResponse = await fetch(dashboardEndpoint);
        const chartResponse = await fetch(chartEndpoint);

        const dashboardJson = await dashboardResponse.json();
        const chartJson = await chartResponse.json();

        setDashboardData(dashboardJson);
        setTopRequestData(chartJson);
      } catch (err) {
        console.error(err);
        setError("Failed to load dashboard");
      }
    };

    loadDashboard();
  }, [selectedType, selectedYear, startDate, endDate]);

  // ======================================================
  // INITIAL LOADING ONLY
  // ======================================================

  if (!dashboardData) {
    return (
      <div className="service-dashboard">
        <h2>Loading Dashboard...</h2>
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
      value: dashboardData?.total_requests?.toLocaleString() || 0,
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
      value: dashboardData?.top_count?.toLocaleString() || 0,
      subtitle: dashboardData?.top_item || "-",
    },
    {
      title: "Total Categories",
      value: dashboardData?.total_categories?.toLocaleString() || 0,
      subtitle: "Available Categories",
    },
  ];

  return (
    <div className="service-dashboard">
      <div className="dashboard-header">
        <h1>Service Ticket Bifurcation</h1>
        <p>Overview of service request bifurcation</p>

        <div className="dashboard-filter">
          <span className="filter-label">Request Type</span>

          <select
            className="filter-select"
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
          >
            <option value="asset">IT Asset Requisition</option>
            <option value="software">Software Requisition</option>
          </select>

          <span className="filter-label">Year</span>

          <select
            className="filter-select"
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
          >
            <option value="all">All</option>
            <option value="2025">2025</option>
            <option value="2026">2026</option>
          </select>

          <span className="filter-label">Date Range</span>

          <div className="date-filter-wrapper">
            <div className="date-range-box">
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />

              <span className="date-arrow">→</span>

              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>

            <button
              className="clear-date-btn"
              onClick={clearDateFilter}
            >
              Clear
            </button>
          </div>
        </div>
      </div>

      <div className="summary-grid">
        {summaryData.map((card, index) => (
          <SummaryCard
            key={index}
            title={card.title}
            value={card.value}
            subtitle={card.subtitle}
          />
        ))}
      </div>

      <div className="top-section">
        <CallCodePieChart
          data={dashboardData?.pie_chart_data || []}
          selectedType={selectedType}
        />

        <TopServiceRequestsChart
          data={topRequestData}
          selectedType={selectedType}
        />
      </div>
    </div>
  );
};

export default ServiceDashboard;