import "../../css/HiringTrendChart.css";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  LabelList
} from "recharts";

const data = [
  { year: "2024", engineers: 26 },
  { year: "2025", engineers: 34 },
  { year: "2026", engineers: 38 },
  { year: "2027 (F)", engineers: 41 },
  { year: "2028 (F)", engineers: 45 }
];

const HiringTrendChart = () => {
  return (
    <div className="chart-card">

      <h3>External Engineers Hired Trend</h3>

      <ResponsiveContainer width="100%" height={260}>
        <BarChart
          data={data}
          margin={{
            top: 20,
            right: 20,
            left: 10,
            bottom: 10
          }}
        >

          <CartesianGrid
            stroke="#e5e7eb"
            strokeDasharray="3 3"
          />

          <XAxis
            dataKey="year"
            tick={{ fontSize: 12 }}
          />

          <YAxis
            tick={{ fontSize: 12 }}
          />

          <Tooltip
            formatter={(value) => [
              value,
              "Engineers"
            ]}
          />

          <Bar
            dataKey="engineers"
            fill="#2563eb"
            radius={[6, 6, 0, 0]}
          >
            <LabelList
              dataKey="engineers"
              position="top"
            />
          </Bar>

        </BarChart>
      </ResponsiveContainer>

    </div>
  );
};

export default HiringTrendChart;