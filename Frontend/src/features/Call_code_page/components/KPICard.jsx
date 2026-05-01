import "../css/KPICard.css";

function KPICard({ total, dominantChannel, percentage }) {
  return (
    <div className="ccb-kpi-row">
      <div className="ccb-kpi-card">
        <div className="ccb-kpi-label">Total Tickets</div>
        <div className="ccb-kpi-value kpi-green">{total.toLocaleString()}</div>
      </div>

      <div className="ccb-kpi-card">
        <div className="ccb-kpi-label">Dominant Channel</div>
        <div className="ccb-kpi-value kpi-dark">{dominantChannel}</div>
      </div>

      <div className="ccb-kpi-card">
        <div className="ccb-kpi-label">Percentage + Share</div>
        <div className="ccb-kpi-value kpi-dark">{percentage}%</div>
      </div>
    </div>
  );
}

export default KPICard;