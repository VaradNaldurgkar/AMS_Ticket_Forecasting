import React, { useEffect, useState } from "react";
import "../../css/InsightCard.css";
import FteModal from "../modal/FteModal";

const AHT = 15;
const WORKING_MINUTES = 8 * 60 * 22;

const InsightCard = () => {
  const [aprilData, setAprilData] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/prediction/actual-vs-predicted")
      .then(res => res.json())
      .then(data => {
        const april = data.data.find(d => d.month === "Apr 2026");
        setAprilData(april);
      })
      .catch(err => console.error(err));
  }, []);

  if (!aprilData) {
    return <div className="insight-card">Loading insight...</div>;
  }

  const { actual, predicted, error } = aprilData;

  const deviation = ((error / actual) * 100).toFixed(1);
  const isHigh = deviation > 20;

  // ✅ FTE CALCULATION
  const totalEffort = predicted * AHT;
  const fte = (totalEffort / WORKING_MINUTES).toFixed(2);
  const engineersRequired = Math.ceil(fte);

  // ✅ CLEAN NUMBER FORMAT (FOR MANAGER READABILITY)
  const formattedEffort = totalEffort.toLocaleString();
  const formattedCapacity = WORKING_MINUTES.toLocaleString();
  const formattedTickets = predicted.toLocaleString();

  // ✅ AI INSIGHT
  const insightText = isHigh
    ? "Potential capacity risk due to abnormal ticket variation."
    : "Workload is within expected range and manageable with planned capacity.";

  const recommendation = isHigh
    ? "Consider buffer staffing or rebalancing workload across teams."
    : "Maintain current staffing levels and monitor trends.";

  const handleViewAnalysis = () => {
    setIsModalOpen(true);
  };

  return (
    <>
      <div className="insight-card">

        <div className="insight-header">
          <span className="icon">⚠️</span>
          <h4>Workforce Insight</h4>
        </div>

        <h3 className="insight-title">
          {isHigh ? "Capacity Risk Detected" : "Capacity Planning Stable"}
        </h3>

        {/* 🔹 SHORT SUMMARY (MANAGER VIEW) */}
        <div className="insight-section">
          <h5>Workforce Requirement</h5>
          <p>
            Based on projected workload, approximately <b>{fte}</b> FTE are required,
            which translates to <b>{engineersRequired} engineers</b> for smooth operations.
          </p>
        </div>

        <div className="insight-section">
          <h5>AI Insight</h5>
          <p>{insightText}</p>
        </div>

        <div className="insight-section">
          <h5>Recommendation</h5>
          <p>{recommendation}</p>
        </div>

        <button className="insight-btn" onClick={handleViewAnalysis}>
          View Full Analysis →
        </button>
      </div>

      {/* ✅ MODAL (WITH DESCRIPTIVE DATA) */}
      <FteModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        data={{
          predicted: formattedTickets,
          totalEffort: formattedEffort,
          fte,
          engineersRequired,
          AHT,
          WORKING_MINUTES: formattedCapacity
        }}
      />
    </>
  );
};

export default InsightCard;