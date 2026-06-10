import "../../css/HeadcountTrendChart.css";

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
  { year: "2024", headcount: 3500 },
  { year: "2025", headcount: 4656 },
  { year: "2026", headcount: 5100 },
  { year: "2027 (F)", headcount: 5600 },
  { year: "2028 (F)", headcount: 6100 }
];

const HeadcountTrendChart = () => {
  return (
    <div className="chart-card">

      <h3>Total Headcount Trend</h3>

      <ResponsiveContainer width="100%" height={260}>
        <LineChart
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
            tickFormatter={(value) =>
              value.toLocaleString()
            }
          />

          <Tooltip
            formatter={(value) => [
              Number(value).toLocaleString(),
              "Headcount"
            ]}
          />

          <Line
            type="monotone"
            dataKey="headcount"
            stroke="#2563eb"
            strokeWidth={3}
            dot={{ r: 5 }}
            activeDot={{ r: 7 }}
          >
            <LabelList
              dataKey="headcount"
              position="top"
              formatter={(value) =>
                Number(value).toLocaleString()
              }
            />
          </Line>

        </LineChart>
      </ResponsiveContainer>

    </div>
  );
};

export default HeadcountTrendChart;