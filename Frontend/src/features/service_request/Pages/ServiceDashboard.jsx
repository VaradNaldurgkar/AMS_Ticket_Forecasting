import { useEffect, useState } from "react";

import SummaryCard from "../components/SummaryCard";
import CallCodePieChart from "../components/CallCodePieChart";
import TopServiceRequestsChart from "../components/TopServiceRequestsChart";

import "../css/serviceDashboard.css";

const ServiceDashboard = () => {

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

    fetch("http://127.0.0.1:8000/api/service/service-breakdown")

      .then((response) => response.json())

      .then((data) => {

        setDashboardData(data);

        setLoading(false);
      })

      .catch((err) => {

        console.error(err);

        setError("Failed to load dashboard");

        setLoading(false);
      });

  }, []);

  // ======================================================
  // LOADING UI
  // ======================================================

  if (loading) {

    return (

      <div className="service-dashboard">

        <h2>Loading Dashboard...</h2>

      </div>
    );
  }

  // ======================================================
  // ERROR UI
  // ======================================================

  if (error) {

    return (

      <div className="service-dashboard">

        <h2>{error}</h2>

      </div>
    );
  }

  // ======================================================
  // SUMMARY DATA
  // ======================================================

  const summaryData = [

    {
      title: "Total Service Tickets",

      value:
        dashboardData.summary_cards.total_tickets.toLocaleString(),

      subtitle: "All generated tickets",
    },

    {
      title: "Most Generated Ticket",

      value:
        dashboardData.summary_cards.top_ticket_count.toLocaleString(),

      subtitle:
        dashboardData.summary_cards.top_ticket.slice(0, 35),
    },

    {
      title: "Total Categories",

      value:
        dashboardData.summary_cards.total_categories.toLocaleString(),

      subtitle: "Service ticket categories",
    },
  ];

  // ======================================================
  // FINAL UI
  // ======================================================

  return (

    <div className="service-dashboard">

      {/* HEADER */}

      <div className="dashboard-header">

        <h1>Service Ticket Bifurcation</h1>

        <p>
          Overview of service request bifurcation
        </p>

      </div>

      {/* SUMMARY CARDS */}

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

      {/* CHART SECTION */}

      <div className="top-section">

        <CallCodePieChart
          data={dashboardData.pie_chart_data}
        />

        <TopServiceRequestsChart
          data={dashboardData.bar_chart_data}
        />

      </div>

    </div>
  );
};

export default ServiceDashboard;