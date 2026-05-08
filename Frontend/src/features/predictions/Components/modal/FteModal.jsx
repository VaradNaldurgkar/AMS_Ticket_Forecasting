import React from "react";
import "../../css/FteModal.css";

export default function FteModal({ isOpen, onClose, data }) {
  if (!isOpen || !data) return null;

  const { assumptions, april, may } = data;

  const renderMonth = (label, d) => (
    <div className="modal-section">
      <h4>{label} 2026</h4>
      <p><b>Predicted Tickets:</b> {d.tickets.toLocaleString()}</p>
      <p><b>Total Effort:</b> {d.totalEffort.toLocaleString()} minutes</p>
      <p><b>FTE Required:</b> {d.fte}</p>
      <p><b>Engineers Needed:</b> {d.engineers}</p>
    </div>
  );

  return (
    <div className="modal-overlay">
      <div className="modal-container">

        <div className="modal-header">
          <h2>FTE Capacity Analysis</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">

          <div className="modal-section">
            <h4>Assumptions Used</h4>
            <p><b>Avg Resolution Time:</b> {assumptions.avgTime} minutes / ticket</p>
            <p><b>Productive Capacity:</b> {assumptions.capacity.toLocaleString()} minutes / engineer / month</p>
          </div>

          <div className="modal-section">
            <h4>Formula</h4>
            <p>
              <b>FTE =</b> (Predicted Tickets × Avg Resolution Time) ÷ Productive Capacity
            </p>
          </div>

          {renderMonth("April", april)}
          {renderMonth("May", may)}

        </div>

        <div className="modal-footer">
          <button className="primary-btn" onClick={onClose}>
            Close
          </button>
        </div>

      </div>
    </div>
  );
}