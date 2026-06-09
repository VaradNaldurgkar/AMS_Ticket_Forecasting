import "../../css/ForecastCalculation.css";

const ForecastCalculation = () => {
  return (
    <div className="forecast-card">

      <h2>How We Calculate Forecast</h2>

      {/* METHOD */}
      <div className="forecast-section">

        <h3>
          1. Hiring Ratio Method (Primary Approach)
        </h3>

        <p>
          We analyze the historical trend of external engineers
          hired as a percentage of total headcount.
        </p>

      </div>

      {/* TABLE */}
      <div className="forecast-table-section">

        <h4>Historical Hiring Ratio</h4>

        <table className="ratio-table">

          <thead>
            <tr>
              <th>Year</th>
              <th>External Engineers</th>
              <th>Headcount</th>
              <th>Hiring Ratio</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>2024</td>
              <td>26</td>
              <td>3,500</td>
              <td>0.74%</td>
            </tr>

            <tr>
              <td>2025</td>
              <td>34</td>
              <td>4,656</td>
              <td>0.73%</td>
            </tr>

            <tr>
              <td>2026</td>
              <td>38</td>
              <td>5,100</td>
              <td>0.75%</td>
            </tr>
          </tbody>

        </table>

      </div>

      {/* AVG RATIO */}
      <div className="average-ratio-box">

        <span>
          Average Hiring Ratio (2024–2026)
        </span>

        <h3>0.74%</h3>

      </div>

      {/* FORECAST LOGIC */}
      <div className="forecast-section">

        <h3>2. Forecast Logic</h3>

        <p>
          Future Headcount is expected to remain stable at
          5,100 (90% certainty).
        </p>

        <p>
          Forecasted Engineers = Headcount × Avg Hiring Ratio
        </p>

      </div>

      {/* FORMULA */}
      <div className="formula-box">
        5,100 × 0.74% ≈ 38 Engineers
      </div>

      {/* HORIZON */}
      <div className="forecast-section">

        <h3>3. Forecast Horizon</h3>

        <p>2027, 2028, 2029</p>

      </div>

      {/* ASSUMPTIONS */}
      <div className="assumption-box">

        <h4>Key Assumptions</h4>

        <ul>
          <li>Headcount remains around 5,100 from 2027 onwards.</li>
          <li>Hiring ratio remains stable.</li>
          <li>No major business strategy changes.</li>
        </ul>

      </div>

      {/* DATA SOURCE */}
      <div className="data-source">

        <h4>Data Source</h4>

        <p>HR / Organization Records</p>

        <p>Years Considered: 2024 – 2026</p>

      </div>

    </div>
  );
};

export default ForecastCalculation;