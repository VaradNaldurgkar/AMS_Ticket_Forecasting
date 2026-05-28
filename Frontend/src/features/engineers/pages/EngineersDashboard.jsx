import React, { useEffect, useState } from "react";

import "../css/EngineersDashboard.css";

import EngineerStats from "../components/EngineerStats";
import WorkforceOverview from "../components/WorkforceOverview";
import FteSummary from "../components/FteSummary";
import FteAnalysisTable from "../components/FteAnalysisTable";
import AssumptionCard from "../components/AssumptionCard";
import CategoryBreakdownTable from "../components/CategoryBreakdownTable";

const EngineersDashboard = () => {

  const [processedData, setProcessedData] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

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

                // ----------------------------------------
                // CALL BACKEND FTE API
                // ----------------------------------------

                const fteResponse =
                  await fetch(
                    `http://127.0.0.1:8000/api/fte/calculate-fte/${tickets}`
                  );

                const fteData =
                  await fteResponse.json();

                console.log(
                  "FTE API RESPONSE:",
                  fteData
                );

                // ----------------------------------------
                // FINAL MONTH OBJECT
                // ----------------------------------------

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

        console.log(
          "FINAL DASHBOARD DATA:",
          dashboardData
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
  // UI
  // ======================================================

  return (

    <div className="engineers-dashboard">

      {/* HEADER */}

      <div className="engineers-header">

        <div className="header-left">

          <h1>Engineers</h1>

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
  />

</div>

{/* CATEGORY BREAKDOWN */}

<div className="category-section">

  <CategoryBreakdownTable
    data={processedData}
  />

</div>

{/* ASSUMPTION CARD */}

<div className="assumption-section">

  <AssumptionCard />

</div>

    </div>

  );

};

export default EngineersDashboard;