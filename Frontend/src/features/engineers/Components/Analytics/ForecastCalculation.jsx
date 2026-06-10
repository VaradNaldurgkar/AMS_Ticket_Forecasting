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

        <h4>Historical & Forecast Hiring Ratio</h4>

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

            {/* Forecast Years */}
            <tr>
              <td>2027</td>
              <td>41</td>
              <td>5,600</td>
              <td>0.74%</td>
            </tr>

            <tr>
              <td>2028</td>
              <td>45</td>
              <td>6,100</td>
              <td>0.74%</td>
            </tr>

          </tbody>

        </table>

      </div>

      {/* AVG RATIO */}
      <div className="average-ratio-box">

        <span>
          Average Hiring Ratio (2024–2028)
        </span>

        <h3>0.74%</h3>

      </div>

      {/* FORECAST LOGIC */}
      <div className="forecast-section">

        <h3>2. Forecast Logic</h3>

        <p>
          Future Headcount is projected to increase by
          approximately 500 employees per year.
        </p>

        <p>
          Forecasted Engineers = Headcount × Average Hiring Ratio
        </p>

      </div>

      {/* FORMULAS */}
      <div className="formula-box">
        <p>2027: 5,600 × 0.74% ≈ 41 Engineers</p>
        <p>2028: 6,100 × 0.74% ≈ 45 Engineers</p>
      </div>

      {/* HORIZON */}
      <div className="forecast-section">

        <h3>3. Forecast Horizon</h3>

        <p>2027 – 2028</p>

      </div>

      {/* ASSUMPTIONS */}
      <div className="assumption-box">

        <h4>Key Assumptions</h4>

        <ul>
          <li>Headcount grows by approximately 500 employees per year.</li>
          <li>Hiring ratio remains stable at around 0.74%.</li>
          <li>No major business strategy or workforce planning changes.</li>
        </ul>

      </div>

      {/* DATA SOURCE */}
      <div className="data-source">

        <h4>Data Source</h4>

        <p>HR / Organization Records</p>

        <p>Historical Years Considered: 2024 – 2026</p>

        <p>Forecast Years: 2027 – 2028</p>

      </div>

    </div>
  );
};

export default ForecastCalculation;