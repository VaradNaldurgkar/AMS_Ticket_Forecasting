import "../../css/HiringRatioChart.css";


import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LabelList
} from "recharts";

const data = [
  { year: "2024", ratio: 0.74 },
  { year: "2025", ratio: 0.73 },
  { year: "2026", ratio: 0.75 },
  { year: "2027(F)", ratio: 0.74 }
];

const HiringRatioChart = () => {
  return (
    <div className="chart-card">
      <h3>Hiring Ratio Trend</h3>

      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="year" />

          <YAxis
            domain={[0.6, 0.8]}
            tickFormatter={(value) => `${value}%`}
          />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="ratio"
            stroke="#8b5cf6"
            strokeWidth={3}
          >
            <LabelList
              dataKey="ratio"
              position="top"
              formatter={(value) => `${value}%`}
            />
          </Line>

        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HiringRatioChart;