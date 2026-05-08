import SummaryCard from "../components/SummaryCard";
import CallCodePieChart from "../components/CallCodePieChart";
import TopServiceRequestsChart from "../components/TopServiceRequestsChart";

import "../css/serviceDashboard.css";

const ServiceDashboard = () => {

  const summaryData = [
    {
      title: "Total Service Tickets",
      value: "17,210",
      subtitle: "All generated tickets",
    },

    {
      title: "Most Generated Ticket",
      value: "2,198",
      subtitle: "IT Asset Requisition",
    },

    {
      title: "Total Categories",
      value: "24",
      subtitle: "Service ticket categories",
    },
  ];

  const pieData = [
    {
      name: "IT Asset",
      tickets: 2198,
    },

    {
      name: "Accounts",
      tickets: 1060,
    },

    {
      name: "MS Teams",
      tickets: 649,
    },

    {
      name: "Software",
      tickets: 196,
    },

    {
      name: "Hardware",
      tickets: 126,
    },
  ];

  const topRequestsData = [
  {
    name: "IT Asset",
    tickets: 2198,
  },

  {
    name: "Accounts",
    tickets: 1060,
  },

  {
    name: "MS Teams",
    tickets: 649,
  },

  {
    name: "Software",
    tickets: 196,
  },

  {
    name: "Hardware",
    tickets: 126,
  },
];

  return (
    <div className="service-dashboard">

      <div className="dashboard-header">

        <h1>Service Ticket Bifurcation</h1>

        <p>
          Overview of service request bifurcation
        </p>

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

        <CallCodePieChart data={pieData} />

        <TopServiceRequestsChart
  data={topRequestsData}
/>

      </div>

    </div>
  );
};

export default ServiceDashboard;