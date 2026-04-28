import "../../css/ErrorAnalysis.css";

const ErrorAnalysis = ({ data }) => {

  const processed = data.map(item => {
    const error = Math.abs(item.actual - item.predicted);
    const percent = ((error / item.actual) * 100).toFixed(1);

    return {
      month: item.month,
      percent: parseFloat(percent),
    };
  });

  const getStatus = (value) => {
    if (value > 10) return "high";
    if (value > 2) return "moderate";
    return "good";
  };

  const getIcon = (status) => {
    if (status === "good") return "✔️";
    if (status === "moderate") return "⚠️";
    return "⚠️";
  };

  return (
    <div className="error-card">

      {/* HEADER */}
      <div className="error-header">
        <h4>Error Analysis</h4>
        <span className="error-sub">(Actual vs Predicted)</span>
      </div>

      {/* ROWS */}
      {processed.map((item, index) => {

        const status = getStatus(item.percent);

        return (
          <div className="error-row" key={index}>

            {/* LEFT SIDE */}
            <div className="error-left">
              <span className={`error-icon ${status}`}>
                {getIcon(status)}
              </span>
              <span className="error-month">{item.month}</span>
            </div>

            {/* BAR */}
            <div className="error-bar-bg">
              <div
                className={`error-bar-fill ${status}`}
                style={{ width: `${Math.min(item.percent * 5, 100)}%` }}
              ></div>
            </div>

            {/* VALUE */}
            <span className={`error-value ${status}`}>
              {item.percent}%
            </span>

          </div>
        );
      })}

      {/* LEGEND */}
      <div className="error-legend">
        <span className="legend-item good">■ Good (&lt;2%)</span>
        <span className="legend-item moderate">■ Moderate (2–10%)</span>
        <span className="legend-item high">■ High (&gt;10%)</span>
      </div>

    </div>
  );
};

export default ErrorAnalysis;