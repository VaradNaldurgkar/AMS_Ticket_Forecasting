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
  { year: "2024", ratio: 74 },
  { year: "2025", ratio: 73 },
  { year: "2026", ratio: 75 },
  { year: "2027 (F)", ratio: 74 },
  { year: "2028 (F)", ratio: 74 }
];

const HiringRatioChart = () => {
  return (
    <div className="chart-card">

      <h3>Hiring Ratio Trend</h3>

      <ResponsiveContainer width="100%" height={280}>
        <LineChart
          data={data}
          margin={{
            top: 30,
            right: 20,
            left: 10,
            bottom: 15
          }}
        >

          <CartesianGrid
            strokeDasharray="3 3"
            vertical={false}
            stroke="#e5e7eb"
          />

          <XAxis
            dataKey="year"
            interval={0}
            tick={{
              fontSize: 12,
              fill: "#475569"
            }}
            axisLine={false}
            tickLine={false}
          />

          <YAxis
            domain={[60, 80]}
            tick={{
              fontSize: 12,
              fill: "#475569"
            }}
            tickFormatter={(value) => `${value}%`}
            axisLine={false}
            tickLine={false}
          />

          <Tooltip
            contentStyle={{
              borderRadius: "10px",
              border: "1px solid #e5e7eb"
            }}
            formatter={(value) => [`${value}%`, "Hiring Ratio"]}
          />

          <Line
            type="monotone"
            dataKey="ratio"
            stroke="#8b5cf6"
            strokeWidth={3}
            dot={{
              r: 5,
              strokeWidth: 3,
              fill: "#fff"
            }}
            activeDot={{
              r: 7
            }}
          >

            <LabelList
              dataKey="ratio"
              position="top"
              offset={10}
              formatter={(value) => `${value}%`}
              style={{
                fill: "#334155",
                fontSize: 12,
                fontWeight: 600
              }}
            />

          </Line>

        </LineChart>
      </ResponsiveContainer>

    </div>
  );
};

export default HiringRatioChart;