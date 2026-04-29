import "../css/InsightCard.css";

function InsightCard({ title, heading, description, recommendation }) {
  return (
    <div className="ccb-insight-card">
      <div className="ccb-insight-title">⚠️ {title}</div>
      <div className="ccb-insight-heading">{heading}</div>

      <p>{description}</p>

      <div className="ccb-insight-subtitle">Recommendation</div>
      <p>{recommendation}</p>

      <button className="ccb-insight-btn">
        View Full Analysis →
      </button>
    </div>
  );
}

export default InsightCard;