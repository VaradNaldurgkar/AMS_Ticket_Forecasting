import React, { useEffect, useState } from "react";

import "../css/FTE_Analysis.css";

import EngineerStats from "../components/EngineerStats";
import WorkforceOverview from "../components/WorkforceOverview";
import FteSummary from "../components/FteSummary";
import FteAnalysisTable from "../components/FteAnalysisTable";
import AssumptionCard from "../components/AssumptionCard";
import CategoryBreakdownModal from "../components/CategoryBreakdownModal";

const EngineersDashboard = () => {

  const [processedData, setProcessedData] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [selectedMonth, setSelectedMonth] =
    useState(null);

  const [isModalOpen, setIsModalOpen] =
    useState(false);

  // ======================================================
  // FETCH FORECAST + FTE ANALYSIS
  // ======================================================

  useEffect(() => {

    const fetchDashboardData = async () => {

      try {

        // ------------------------------------------------
        // FETCH MONTHLY FORECAST
        // ------------------------------------------------

        const forecastResponse =
          await fetch(
            "http://127.0.0.1:8000/api/prediction/future"
          );

        const forecastJson =
          await forecastResponse.json();

        const forecastData =
          Array.isArray(forecastJson)
            ? forecastJson
            : forecastJson.data;

        if (!Array.isArray(forecastData)) {

          console.error(
            "Invalid forecast response"
          );

          return;

        }

        // ------------------------------------------------
        // FETCH FTE ANALYSIS FOR EACH MONTH
        // ------------------------------------------------

        const dashboardData =
          await Promise.all(

            forecastData.map(
              async (row) => {

                const tickets =
                  row?.predicted ??
                  row?.tickets ??
                  row?.forecast ??
                  0;

                const fteResponse =
                  await fetch(
                    `http://127.0.0.1:8000/api/fte/calculate-fte/${tickets}`
                  );

                const fteData =
                  await fteResponse.json();

                console.log("Tickets:", tickets);
console.log("FTE API Response:", fteData);

                return {

                  month:
                    row.month,

                  tickets,

                  totalEffort:
                    fteData.total_effort,

                  fte:
                    fteData.fte_required,

                  engineers:
                    fteData.engineers_required,

                  capacity:
                    fteData.capacity_available,

                  utilization:
                    fteData.utilization,

                  prioritySummary:
                    fteData.priority_summary,

                  workloadBreakdown:
                    fteData.workload_breakdown

                };

              }
            )
          );

        setProcessedData(
          dashboardData
        );

      } catch (error) {

        console.error(
          "Dashboard fetch failed:",
          error
        );

      } finally {

        setLoading(false);

      }

    };

    fetchDashboardData();

  }, []);

  // ======================================================
  // MODAL HANDLERS
  // ======================================================

  const handleViewBreakdown = (
    month
  ) => {

    setSelectedMonth(
      month
    );

    setIsModalOpen(
      true
    );

  };

  const closeModal = () => {

    setSelectedMonth(
      null
    );

    setIsModalOpen(
      false
    );

  };

  // ======================================================
  // LOADING STATE
  // ======================================================

  if (loading) {

    return (

      <div className="engineers-dashboard">

        <div className="loading-state">

          Loading workforce analytics...

        </div>

      </div>

    );

  }

  // ======================================================
  // SELECTED MONTH DATA
  // ======================================================

  const selectedMonthData =
    processedData.find(
      item =>
        item.month === selectedMonth
    );

  // ======================================================
  // UI
  // ======================================================

  return (

    <div className="engineers-dashboard">

      {/* HEADER */}

      <div className="engineers-header">

        <div className="header-left">

          <h1>FTE Analysis</h1>

          <p>
            Workforce capacity planning and FTE analysis
          </p>

        </div>

      </div>

      {/* TOP STATS */}

      <EngineerStats
        data={processedData}
      />

      {/* MIDDLE SECTION */}

      <div className="middle-grid">

        <WorkforceOverview
          data={processedData}
        />

        <FteSummary
          data={processedData}
        />

      </div>

      {/* FTE TABLE */}

      <div className="fte-table-section">

        <FteAnalysisTable
          data={processedData}
          onViewBreakdown={
            handleViewBreakdown
          }
        />

      </div>

      {/* BREAKDOWN MODAL */}

      <CategoryBreakdownModal

        isOpen={
          isModalOpen
        }

        month={
          selectedMonth
        }

        data={
          selectedMonthData
            ?.workloadBreakdown || []
        }

        onClose={
          closeModal
        }

      />

      {/* ASSUMPTION CARD */}

      <div className="assumption-section">

        <AssumptionCard />

      </div>

    </div>

  );

};

export default EngineersDashboard;