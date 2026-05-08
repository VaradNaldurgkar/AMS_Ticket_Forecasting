import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
} from "recharts";

const COLORS = [
  "#00A76F",
  "#3B82F6",
  "#8B5CF6",
  "#F59E0B",
  "#EF4444",
];

const CallCodePieChart = ({ data }) => {
  return (
    <div className="chart-card">

      <h2>Bifurcation by Call Code</h2>

      <div className="pie-chart-wrapper">

        <PieChart width={300} height={250}>

          <Pie
            data={data}
            dataKey="tickets"
            nameKey="name"
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={85}
          >

            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={COLORS[index % COLORS.length]}
              />
            ))}

          </Pie>

          <Tooltip />

        </PieChart>

        <div className="pie-legend">

          {data.map((item, index) => (

            <div className="legend-item" key={index}>

              <div
                className="legend-color"
                style={{
                  background:
                    COLORS[index % COLORS.length],
                }}
              />

              <span className="legend-name">
                {item.name}
              </span>

              <span className="legend-value">
                {item.tickets}
              </span>

            </div>

          ))}

        </div>

      </div>

    </div>
  );
};

export default CallCodePieChart;