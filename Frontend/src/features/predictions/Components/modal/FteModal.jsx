import React from "react";
import "../../css/FteModal.css";

export default function FteModal({ isOpen, onClose, data }) {
  if (!isOpen || !data) return null;

  const {
    predicted,
    totalEffort,
    fte,
    engineersRequired,
    AHT,
    WORKING_MINUTES
  } = data;

  return (
    <div className="modal-overlay">
      <div className="modal-container">

        <div className="modal-header">
          <h2>FTE Analysis - April 2026</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">

          <div className="modal-section">
            <h4>Workload</h4>
            <p><b>Predicted Tickets:</b> {predicted}</p>
            <p><b>Avg Handling Time:</b> {AHT} mins</p>
            <p><b>Total Effort:</b> {totalEffort} mins</p>
          </div>

          <div className="modal-section">
            <h4>Capacity</h4>
            <p><b>Per Engineer Capacity:</b> {WORKING_MINUTES} mins/month</p>
          </div>

          <div className="modal-section highlight">
            <h4>Workforce Requirement</h4>
            <p><b>FTE Required:</b> {fte}</p>
            <p><b>Engineers Needed:</b> {engineersRequired}</p>
          </div>

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