import "../../css/PredictionTable.css";

const PredictionTable = ({ data }) => {

  // Helper to format month
  const formatMonth = (month) => {
    return new Date(month).toLocaleString("default", {
      month: "short",
      year: "numeric",
    });
  };

  return (
    <div className="table-container">
      <h3>Prediction vs Actual (Jan–April 2026)</h3>

      <table>
        <thead>
          <tr>
            <th>Month</th>
            <th>Total Tickets</th>
            <th>Predicted Tickets</th>
            <th>Absolute Error</th>
          </tr>
        </thead>

        <tbody>
          {data.map((row, index) => {
            const absoluteError = Math.abs(row.actual - row.predicted);

            return (
              <tr key={index}>
                <td>{row.month}</td>
                <td>{row.actual}</td>
                <td>{row.predicted}</td>
                <td>{absoluteError.toFixed(2)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default PredictionTable;