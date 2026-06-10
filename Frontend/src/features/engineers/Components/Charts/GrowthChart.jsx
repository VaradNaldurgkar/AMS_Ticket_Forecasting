import "../../css/GrowthChart.css";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LabelList,
  Legend
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
  },
  {
    year: "2026→2027",
    headcount: 9.80,
    hiring: 7.89
  },
  {
    year: "2027→2028",
    headcount: 8.93,
    hiring: 9.76
  }
];

const GrowthChart = () => {
  return (
    <div className="chart-card">

      <h3>Year over Year Growth (%)</h3>

      <ResponsiveContainer width="100%" height={300}>
  <BarChart
    data={data}
    margin={{
      top: 30,
      right: 20,
      left: 10,
      bottom: 30
    }}
    barCategoryGap="25%"
  >
    <CartesianGrid
      strokeDasharray="3 3"
      vertical={false}
      stroke="#e5e7eb"
    />

    <XAxis
      dataKey="year"
      tick={{ fontSize: 13, fill: "#475569" }}
      axisLine={false}
      tickLine={false}
    />

    <YAxis
      tick={{ fontSize: 13, fill: "#475569" }}
      axisLine={false}
      tickLine={false}
      tickFormatter={(value) => `${value}%`}
    />

    <Tooltip
      contentStyle={{
        borderRadius: "10px",
        border: "1px solid #e5e7eb"
      }}
      formatter={(value) => [`${value}%`]}
    />

    <Legend
      verticalAlign="top"
      height={40}
      iconType="circle"
      wrapperStyle={{
        fontSize: "13px"
      }}
    />

    <Bar
      dataKey="headcount"
      name="Headcount Growth"
      fill="#2563eb"
      radius={[6, 6, 0, 0]}
      maxBarSize={36}
    >
      <LabelList
        dataKey="headcount"
        position="top"
        offset={8}
        formatter={(value) => `${value}%`}
        style={{
          fontSize: 12,
          fill: "#334155",
          fontWeight: 600
        }}
      />
    </Bar>

    <Bar
      dataKey="hiring"
      name="Hiring Growth"
      fill="#22c55e"
      radius={[6, 6, 0, 0]}
      maxBarSize={36}
    >
      <LabelList
        dataKey="hiring"
        position="top"
        offset={8}
        formatter={(value) => `${value}%`}
        style={{
          fontSize: 12,
          fill: "#334155",
          fontWeight: 600
        }}
      />
    </Bar>

  </BarChart>
</ResponsiveContainer>

    </div>
  );
};

export default GrowthChart;