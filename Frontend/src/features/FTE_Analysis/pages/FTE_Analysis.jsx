import React, { useEffect, useState } from "react";

import "../css/FTE_Analysis.css";

import EngineerStats from "../components/EngineerStats";
import WorkforceOverview from "../components/WorkforceOverview";
import FteSummary from "../components/FteSummary";
import FteAnalysisTable from "../components/FteAnalysisTable";
import CategoryBreakdownModal from "../components/CategoryBreakdownModal";

const EngineersDashboard = () => {

  const [processedData, setProcessedData] = useState([]);

  const [loading, setLoading] = useState(true);

  const [selectedMonth, setSelectedMonth] = useState(null);

  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {

    const fetchDashboardData = async () => {

      try {

        const historicalResponse = await fetch(
          "http://127.0.0.1:8000/api/fte/historical-pune"
        );

        if (!historicalResponse.ok) {
          throw new Error(
            `Historical API failed: ${historicalResponse.status}`
          );
        }

        const historicalJson =
          await historicalResponse.json();

        const historicalData =
          Array.isArray(historicalJson)
            ? historicalJson
            : historicalJson.data || [];

        console.log(
          "Historical Data:",
          historicalData
        );

        const forecastResponse = await fetch(
          "http://127.0.0.1:8000/api/prediction/future"
        );

        if (!forecastResponse.ok) {
          throw new Error(
            `Forecast API failed: ${forecastResponse.status}`
          );
        }

        const forecastJson =
          await forecastResponse.json();

        const forecastData =
          Array.isArray(forecastJson)
            ? forecastJson
            : forecastJson.data || forecastJson.future_forecast || [];

        if (!Array.isArray(forecastData)) {
          throw new Error(
            "Invalid forecast response"
          );
        }

        const formattedHistoricalData =
          historicalData
            .map((row) => ({
              month: row.month,
              tickets: Number(
                row.tickets ??
                row.Total_Tickets ??
                row.total_tickets ??
                0
              )
            }))
            .filter(
              row =>
                row.month &&
                Number.isFinite(row.tickets)
            );

        const formattedForecastData =
          forecastData
            .map((row) => ({
              month: row.month,
              tickets: Number(
                row.predicted ??
                row.tickets ??
                row.forecast ??
                0
              )
            }))
            .filter(
              row =>
                row.month &&
                Number.isFinite(row.tickets)
            );

        console.log(
          "Formatted Historical Data:",
          formattedHistoricalData
        );

        console.log(
          "Formatted Forecast Data:",
          formattedForecastData
        );

        const monthMap = new Map();

        formattedHistoricalData.forEach(row => {

          monthMap.set(
            row.month,
            row
          );

        });

        formattedForecastData.forEach(row => {

          if (!monthMap.has(row.month)) {

            monthMap.set(
              row.month,
              row
            );

          }

        });

        const allMonths =
          Array.from(
            monthMap.values()
          ).sort(
            (a, b) =>
              new Date(a.month) -
              new Date(b.month)
          );

        console.log(
          "Combined Months:",
          allMonths
        );

        const dashboardData =
          await Promise.all(

            allMonths.map(
              async (row) => {

                const tickets =
                  Number(row.tickets);

                const fteResponse =
                  await fetch(
                    `http://127.0.0.1:8000/api/fte/calculate-fte/${tickets}`
                  );

                if (!fteResponse.ok) {

                  throw new Error(
                    `FTE API failed for ${row.month}: ${fteResponse.status}`
                  );

                }

                const fteData =
                  await fteResponse.json();

                console.log(
                  "================================="
                );

                console.log(
                  "Month:",
                  row.month
                );

                console.log(
                  "Tickets:",
                  tickets
                );

                console.log(
                  "FULL FTE DATA:",
                  fteData
                );

                console.log(
                  "================================="
                );

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

                  availableEngineers:
                    fteData.available_engineers,

                  avgProductivity:
                    fteData.avg_productivity,

                  monthlyCapacity:
                    fteData.monthly_capacity,

                  requiredTicketsPerEngineer:
                    fteData.required_tickets_per_engineer,

                  engineerGap:
                    fteData.engineer_gap,

                  ticketGap:
                    fteData.ticket_gap,

                  productivityIncreaseNeeded:
                    fteData.productivity_increase_needed,

                  productivityGap:
                    fteData.productivity_gap,

                  prioritySummary:
                    fteData.priority_summary,

                  workloadBreakdown:
                    fteData.workload_breakdown

                };

              }
            )
          );

        console.log(
          "FINAL dashboardData:",
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

  const handleViewBreakdown = (
    month
  ) => {

    console.log(
      "Clicked Month:",
      month
    );

    setSelectedMonth(
      month
    );

    setIsModalOpen(
      true
    );

  };

  const closeModal = () => {

    setSelectedMonth(null);

    setIsModalOpen(false);

  };

  if (loading) {

    return (

      <div className="engineers-dashboard">

        <div className="loading-state">

          Loading workforce analytics...

        </div>

      </div>

    );

  }

  const selectedMonthData =
    processedData.find(
      item =>
        item.month ===
        selectedMonth
    );

  return (

    <div className="engineers-dashboard">

      <div className="engineers-header">

        <div className="header-left">

          <h1>
            FTE Analysis
          </h1>

          <p>
            Workforce capacity planning and FTE analysis
          </p>

        </div>

      </div>

      <EngineerStats
        data={processedData}
      />

      <div className="middle-grid">

        <WorkforceOverview
          data={processedData}
        />

        <FteSummary
          data={processedData}
        />

      </div>

      <div className="fte-table-section">

        <FteAnalysisTable
          data={processedData}
          onViewBreakdown={
            handleViewBreakdown
          }
        />

      </div>

      <CategoryBreakdownModal
        isOpen={isModalOpen}
        month={selectedMonth}
        workforceData={selectedMonthData}
        onClose={closeModal}
      />

    </div>

  );

};

export default EngineersDashboard;