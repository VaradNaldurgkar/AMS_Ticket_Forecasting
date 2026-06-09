import "../../css/GrowthChart.css";


import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LabelList
} from "recharts";

const data = [
  {
    year: "2024→2025",
    headcount: 33.03,
    hiring: 30.77
  },
  {
    year: "2025→2026",
    headcount: 9.54,
    hiring: 11.76
  }
];

const GrowthChart = () => {
  return (
    <div className="chart-card">
      <h3>Year over Year Growth (%)</h3>

      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="year" />

          <YAxis />

          <Tooltip />

          <Bar
            dataKey="headcount"
            fill="#2563eb"
          >
            <LabelList
              dataKey="headcount"
              position="top"
            />
          </Bar>

          <Bar
            dataKey="hiring"
            fill="#22c55e"
          >
            <LabelList
              dataKey="hiring"
              position="top"
            />
          </Bar>

        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GrowthChart;