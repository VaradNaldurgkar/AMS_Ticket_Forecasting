import React, { useCallback, useEffect, useState } from "react";
import axios from "axios";

import MetricCards from "../components/MetricCards";
import IncidentBarChart from "../components/IncidentBarChart";
import StatusTable from "../components/StatusTable";

import "../css/IncidentDashboard.css";

// ======================================================
// API URL
// ======================================================

const API_URL =
  "http://127.0.0.1:8000/api/incident-dashboard";


// ======================================================
// COMPONENT
// ======================================================

const IncidentDashboard = () => {

  // ======================================================
  // DASHBOARD STATE
  // ======================================================

  const [dashboardData, setDashboardData] = useState(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  // ======================================================
  // FILTER STATE
  // ======================================================

  const [selectedYear, setSelectedYear] = useState("");

  const [startDate, setStartDate] = useState("");

  const [endDate, setEndDate] = useState("");


  // ======================================================
  // FETCH DASHBOARD DATA
  // ======================================================

  const fetchDashboardData = useCallback(
    async (filters = {}) => {

      try {

        setLoading(true);

        setError("");

        // ------------------------------------------------
        // Build query parameters
        // ------------------------------------------------

        const params = {};

        if (filters.year) {

          params.year = filters.year;

        }

        if (filters.start_date) {

          params.start_date = filters.start_date;

        }

        if (filters.end_date) {

          params.end_date = filters.end_date;

        }

        // ------------------------------------------------
        // API REQUEST
        // ------------------------------------------------

        const response = await axios.get(
          API_URL,
          {
            params: params
          }
        );

        setDashboardData(response.data);

      } catch (err) {

        console.error(
          "Incident dashboard error:",
          err
        );

        setError(
          "Failed to load incident dashboard data."
        );

      } finally {

        setLoading(false);

      }

    },
    []
  );


  // ======================================================
  // INITIAL LOAD
  // ======================================================

  useEffect(() => {

    fetchDashboardData();

  }, [fetchDashboardData]);


  // ======================================================
  // REFRESH WHEN USER RETURNS TO DASHBOARD
  //
  // Useful when:
  // 1. User uploads an Excel file
  // 2. Master CSV is updated
  // 3. User navigates back to this page
  //
  // No date/year is hardcoded.
  // ======================================================

  useEffect(() => {

    const handleWindowFocus = () => {

      fetchDashboardData({

        year: selectedYear,

        start_date: startDate,

        end_date: endDate

      });

    };

    window.addEventListener(
      "focus",
      handleWindowFocus
    );

    return () => {

      window.removeEventListener(
        "focus",
        handleWindowFocus
      );

    };

  }, [
    fetchDashboardData,
    selectedYear,
    startDate,
    endDate
  ]);


  // ======================================================
  // APPLY FILTERS
  // ======================================================

  const handleApplyFilters = () => {

    fetchDashboardData({

      year: selectedYear,

      start_date: startDate,

      end_date: endDate

    });

  };


  // ======================================================
  // CLEAR FILTERS
  // ======================================================

  const handleClearFilters = () => {

    setSelectedYear("");

    setStartDate("");

    setEndDate("");

    fetchDashboardData();

  };


  // ======================================================
  // LOADING
  // ======================================================

  if (loading && !dashboardData) {

    return (

      <div className="incident-dashboard">

        <h2>
          Loading dashboard...
        </h2>

      </div>

    );

  }


  // ======================================================
  // ERROR
  // ======================================================

  if (error && !dashboardData) {

    return (

      <div className="incident-dashboard">

        <h2>
          {error}
        </h2>

      </div>

    );

  }


  // ======================================================
  // API DATA
  // ======================================================

  const summaryCards =
    dashboardData?.summary_cards || {};

  const chartData =
    dashboardData?.chart_data || [];

  const tableData =
    dashboardData?.table_data || [];


  // ======================================================
  // AVAILABLE FILTER DATA
  //
  // EVERYTHING COMES FROM BACKEND
  //
  // Nothing is hardcoded.
  // ======================================================

  const availableYears =
    dashboardData?.available_filters?.years || [];

  const minimumDate =
    dashboardData?.available_filters?.min_date || "";

  const maximumDate =
    dashboardData?.available_filters?.max_date || "";


  // ======================================================
  // REMOVE GENERAL / UNCATEGORIZED
  // FROM CHART ONLY
  // ======================================================

  const filteredChartData =
    chartData.filter(
      (item) =>
        item.name !== "General / Uncategorized"
    );


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

            Overview of incident requests by category
            and resolution metrics

          </p>

        </div>

      </div>


      {/* ================================================= */}
      {/* FILTERS */}
      {/* ================================================= */}

      <div className="incident-dashboard__filters">


        {/* =============================================== */}
        {/* YEAR */}
        {/* =============================================== */}

        <div className="incident-dashboard__filter-group">

          <label
            className="incident-dashboard__filter-label"
          >
            Year
          </label>

          <select
            className="incident-dashboard__filter-select"
            value={selectedYear}
            onChange={(e) => {

              setSelectedYear(
                e.target.value
              );

            }}
          >

            <option value="">
              All Years
            </option>

            {availableYears.map(
              (year) => (

                <option
                  key={year}
                  value={year}
                >
                  {year}
                </option>

              )
            )}

          </select>

        </div>


        {/* =============================================== */}
        {/* START DATE */}
        {/* =============================================== */}

        <div className="incident-dashboard__filter-group">

          <label
            className="incident-dashboard__filter-label"
          >
            Start Date
          </label>

          <input
            className="incident-dashboard__filter-input"
            type="date"
            value={startDate}
            min={minimumDate}
            max={
              endDate ||
              maximumDate
            }
            onChange={(e) =>
              setStartDate(
                e.target.value
              )
            }
          />

        </div>


        {/* =============================================== */}
        {/* END DATE */}
        {/* =============================================== */}

        <div className="incident-dashboard__filter-group">

          <label
            className="incident-dashboard__filter-label"
          >
            End Date
          </label>

          <input
            className="incident-dashboard__filter-input"
            type="date"
            value={endDate}
            min={
              startDate ||
              minimumDate
            }
            max={maximumDate}
            onChange={(e) =>
              setEndDate(
                e.target.value
              )
            }
          />

        </div>


        {/* =============================================== */}
        {/* ACTION BUTTONS */}
        {/* =============================================== */}

        <div className="incident-dashboard__filter-actions">

          <button
            className="incident-dashboard__apply-btn"
            onClick={handleApplyFilters}
            disabled={loading}
          >

            {loading
              ? "Loading..."
              : "Apply Filters"}

          </button>


          <button
            className="incident-dashboard__clear-btn"
            onClick={handleClearFilters}
            disabled={loading}
          >

            Clear

          </button>

        </div>

      </div>


      {/* ================================================= */}
      {/* DATA RANGE INFORMATION */}
      {/* ================================================= */}

      {minimumDate &&
        maximumDate && (

          <div className="incident-dashboard__data-range">

            Data available from{" "}

            <strong>
              {minimumDate}
            </strong>

            {" "}to{" "}

            <strong>
              {maximumDate}
            </strong>

          </div>

        )}


      {/* ================================================= */}
      {/* REFRESH INDICATOR */}
      {/* ================================================= */}

      {loading && dashboardData && (

        <div className="incident-dashboard__loading-indicator">

          Updating dashboard...

        </div>

      )}


      {/* ================================================= */}
      {/* METRIC CARDS */}
      {/* ================================================= */}

      <MetricCards
        data={summaryCards}
      />


      {/* ================================================= */}
      {/* CHART + TABLE */}
      {/* ================================================= */}

      <div className="incident-dashboard__row-2">


        {/* =============================================== */}
        {/* BAR CHART */}
        {/* =============================================== */}

        <IncidentBarChart
          data={filteredChartData}
        />


        {/* =============================================== */}
        {/* TABLE */}
        {/* =============================================== */}

        <StatusTable
          data={tableData}
        />

      </div>


    </div>

  );

};


export default IncidentDashboard;