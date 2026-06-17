import { useState } from "react";
import "../../css/ForecastCalculation.css";

const ForecastCalculation = () => {

  const [selectedYear, setSelectedYear] =
    useState(null);

  const ratioData = [
  {
    year: "2024",
    engineers: 26,
    headcount: 3500,
    ratio: "0.74%",
    tickets: 16328,
    ticketsPerEngineer: 628,
    monthlyTicketsPerEngineer: 52.33
  },
  {
    year: "2025",
    engineers: 34,
    headcount: 4656,
    ratio: "0.73%",
    tickets: 17100,
    ticketsPerEngineer: 503,
    monthlyTicketsPerEngineer: 41.92
  },
  {
    year: "2026",
    engineers: 38,
    headcount: 5100,
    ratio: "0.75%",
    tickets: 16117,
    ticketsPerEngineer: 424,
    monthlyTicketsPerEngineer: 35.33
  },
  {
    year: "2027",
    engineers: 41,
    headcount: 5600,
    ratio: "0.74%"
  },
  {
    year: "2028",
    engineers: 45,
    headcount: 6100,
    ratio: "0.74%"
  }
];

  return (

    <div className="forecast-card">

      <h2>How We Calculate Forecast</h2>

      {/* METHOD */}

      <div className="forecast-section">

        <h3>
          1. Hiring Ratio Method (Primary Approach)
        </h3>

        <p>
          We analyze the historical trend of
          external engineers hired as a
          percentage of total headcount.
        </p>

      </div>

      {/* TABLE */}

      <div className="forecast-table-section">

        <h4>
          Historical & Forecast Hiring Ratio
        </h4>

        <table className="ratio-table">

          <thead>

            <tr>

              <th>Year</th>

              <th>
                External Engineers
              </th>

              <th>
                Headcount
              </th>

              <th>
                Hiring Ratio
              </th>

              <th>
                Info
              </th>

            </tr>

          </thead>

          <tbody>

            {ratioData.map((row) => (

              <tr key={row.year}>

                <td>{row.year}</td>

                <td>
                  {row.engineers}
                </td>

                <td>
                  {row.headcount.toLocaleString()}
                </td>

                <td>
                  {row.ratio}
                </td>

                <td>

                  <button
                    className="ratio-info-btn"
                    onClick={() =>
                      setSelectedYear(row)
                    }
                    title="View Calculation"
                  >
                    i
                  </button>

                </td>

              </tr>

            ))}

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
          Future Headcount is projected to
          increase by approximately
          500 employees per year.
        </p>

        <p>
          Forecasted Engineers =
          Headcount × Average Hiring Ratio
        </p>

      </div>

      {/* FORMULAS */}

      <div className="formula-box">

        <p>
          2027: 5,600 × 0.74% ≈ 41 Engineers
        </p>

        <p>
          2028: 6,100 × 0.74% ≈ 45 Engineers
        </p>

      </div>

      {/* HORIZON */}

      <div className="forecast-section">

        <h3>
          3. Forecast Horizon
        </h3>

        <p>
          2027 – 2028
        </p>

      </div>

      {/* ASSUMPTIONS */}

      <div className="assumption-box">

        <h4>
          Key Assumptions
        </h4>

        <ul>

          <li>
            Headcount grows by
            approximately 500 employees
            per year.
          </li>

          <li>
            Hiring ratio remains stable
            at around 0.74%.
          </li>

          <li>
            No major business strategy
            or workforce planning changes.
          </li>

        </ul>

      </div>

      {/* DATA SOURCE */}

      <div className="data-source">

        <h4>
          Data Source
        </h4>

        <p>
          HR / Organization Records
        </p>

        <p>
          Historical Years Considered:
          2024 – 2026
        </p>

        <p>
          Forecast Years:
          2027 – 2028
        </p>

      </div>

      {/* ========================================= */}
      {/* MODAL */}
      {/* ========================================= */}

      {selectedYear && (

        <div
          className="ratio-modal-overlay"
          onClick={() =>
            setSelectedYear(null)
          }
        >

          <div
            className="ratio-modal"
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            <button
              className="ratio-close"
              onClick={() =>
                setSelectedYear(null)
              }
            >
              ✕
            </button>

            <h2>
              Hiring Ratio Analysis
              ({selectedYear.year})
            </h2>

            <div className="modal-section">

  <h3>Workforce Snapshot</h3>

  <p>
    Total Tickets Received:
    <strong>
      {" "}
      {selectedYear.tickets?.toLocaleString() || "-"}
    </strong>
  </p>

  <p>
    ATOS Engineers:
    <strong>
      {" "}
      {selectedYear.engineers}
    </strong>
  </p>

  <p>
    Organization Headcount:
    <strong>
      {" "}
      {selectedYear.headcount.toLocaleString()}
    </strong>
  </p>

  <p>
    Hiring Ratio:
    <strong>
      {" "}
      {selectedYear.ratio}
    </strong>
  </p>

</div>

<div className="modal-section">

  <h3>Hiring Ratio Calculation</h3>

  <p>
    External Engineers ÷ Headcount
  </p>

  <p>

    {selectedYear.engineers}
    {" ÷ "}
    {selectedYear.headcount.toLocaleString()}
    {" = "}
    {selectedYear.ratio}

  </p>

</div>

{selectedYear.tickets && (

  <>

    <div className="modal-section">

      <h3>
        Ticket Load Calculation
      </h3>

      <p>

        Annual Tickets Per Engineer

      </p>

      <p>

        {selectedYear.tickets.toLocaleString()}
        {" ÷ "}
        {selectedYear.engineers}
        {" = "}
        <strong>
          {selectedYear.ticketsPerEngineer}
        </strong>

      </p>

      <p>

        Monthly Tickets Per Engineer

      </p>

      <p>

        {selectedYear.ticketsPerEngineer}
        {" ÷ 12 = "}
        <strong>
          {selectedYear.monthlyTicketsPerEngineer}
        </strong>
        {" tickets/month"}

      </p>

    </div>

    <div className="modal-section">

      <h3>
        Engineer Capacity Analysis
      </h3>

      <p>

        AMS support engineers generally
        handle between
        <strong>
          {" "}40–70 tickets per month
        </strong>
        {" "}
        depending on ticket complexity.

      </p>

      <p>

        Actual observed workload:

      </p>

      <p>

        <strong>
          {selectedYear.monthlyTicketsPerEngineer}
        </strong>
        {" "}
        tickets per engineer per month.

      </p>

     

    </div>

    <div className="modal-section">

      <h3>
        Management Interpretation
      </h3>

      <p>

        Total tickets received during
        {` ${selectedYear.year} `}
        were

        <strong>
          {" "}
          {selectedYear.tickets.toLocaleString()}
        </strong>

      </p>

      <p>

        Supported by

        <strong>
          {" "}
          {selectedYear.engineers}
          {" "}ATOS engineers
        </strong>

      </p>

      <p>

        Resulting in

        <strong>
          {" "}
          {selectedYear.monthlyTicketsPerEngineer}
          {" "}tickets per engineer
          per month
        </strong>

      </p>

      <p>

        Based purely on ticket volume,
        the engineering team appears
        adequately staffed and capable
        of handling the incoming AMS
        workload.

      </p>

    </div>

  </>

)}

<div className="modal-warning">

  <h3>
    Important Limitation
  </h3>

  <p>

    This assessment is based on
    ticket volume only.

  </p>

  <p>

    Actual productivity cannot be
    measured because engineer
    worklogs, utilization reports,
    effort tracking and timesheet
    data are currently unavailable.

  </p>

  <p>

    Once productivity metrics become
    available, this analysis can be
    upgraded to a true workforce
    capacity model.

  </p>

</div>

          </div>

        </div>

      )}

    </div>

  );

};

export default ForecastCalculation;