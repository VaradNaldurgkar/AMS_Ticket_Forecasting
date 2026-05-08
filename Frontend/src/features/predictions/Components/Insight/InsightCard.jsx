import React, { useEffect, useState } from "react";
import "../../css/InsightCard.css";
import FteModal from "../modal/FteModal";

const AVG_RESOLUTION_TIME = 110;
const PRODUCTIVE_MINUTES = 7400;

const InsightCard = () => {
  const [forecastData, setForecastData] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/prediction/future")
      .then(res => res.json())
      .then(res => {
        console.log("✅ Future API response:", res);

        // ✅ HANDLE BOTH RESPONSE SHAPES
        const data = Array.isArray(res) ? res : res.data;

        if (!Array.isArray(data)) {
          console.error("❌ Future API returned invalid data:", res);
          setForecastData([]); // prevent infinite loading
          return;
        }

        setForecastData(data);
      })
      .catch(err => {
        console.error("❌ Forecast fetch failed:", err);
        setForecastData([]); // prevent infinite loading
      });
  }, []);

  if (!forecastData) {
    return <div className="insight-card">Loading workforce insight…</div>;
  }

  // ✅ First two months = April + May (same order as forecast card)
  const aprilRow = forecastData[0];
  const mayRow = forecastData[1];

  const getTickets = row =>
    row?.predicted ??
    row?.tickets ??
    row?.forecast ??
    0;

  const calculateFte = tickets => {
    const totalEffort = tickets * AVG_RESOLUTION_TIME;
    const fte = totalEffort / PRODUCTIVE_MINUTES;

    return {
      tickets,
      totalEffort,
      fte: fte.toFixed(2),
      engineers: Math.ceil(fte)
    };
  };

  const april = calculateFte(getTickets(aprilRow));
  const may = calculateFte(getTickets(mayRow));

  return (
    <>
      <div className="insight-card">
        <div className="insight-header">
          <span className="icon"></span>
          <h4>Workforce Insight</h4>
        </div>

        <h3 className="insight-title">Capacity Planning Overview</h3>

        <div className="insight-section">
          <h5>Workforce Requirement</h5>

          <p>
            <b>{aprilRow?.month}:</b>{" "}
            {april.tickets.toLocaleString()} tickets →
            <b> {april.engineers} engineers</b>
          </p>

          <p>
            <b>{mayRow?.month}:</b>{" "}
            {may.tickets.toLocaleString()} tickets →
            <b> {may.engineers} engineers</b>
          </p>
        </div>

        <button
          className="insight-btn"
          onClick={() => setIsModalOpen(true)}
        >
          View Full Analysis →
        </button>
      </div>

      <FteModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        data={{
          assumptions: {
            avgTime: AVG_RESOLUTION_TIME,
            capacity: PRODUCTIVE_MINUTES
          },
          april,
          may
        }}
      />
    </>
  );
};

export default InsightCard;