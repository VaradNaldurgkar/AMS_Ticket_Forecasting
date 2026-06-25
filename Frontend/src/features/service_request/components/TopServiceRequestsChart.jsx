import {
  BarChart,
  Bar,
 XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

const TopServiceRequestsChart = ({
  data,
  selectedType,
}) => {

  // Only top 10 records
  const chartData = data.slice(0, 10);

  return (
    <div className="chart-card">

      <h2>
        {selectedType === "asset"
          ? "Top Requested Assets"
          : "Top Requested Software"}
      </h2>

      <ResponsiveContainer
        width="100%"
        height={320}
      >
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{
            top: 10,
            right: 20,
            left: 40,
            bottom: 10,
          }}
        >

          <CartesianGrid
            strokeDasharray="3 3"
            horizontal={false}
          />

          <XAxis
            type="number"
            tick={{ fontSize: 12 }}
          />

          <YAxis
            type="category"
            dataKey="name"
            tick={{ fontSize: 12 }}
            width={180}
          />

          <Tooltip
            formatter={(value) => [
              value,
              "Count",
            ]}
          />

          <Bar
            dataKey="count"
            fill="#00A76F"
            radius={[0, 6, 6, 0]}
          />

        </BarChart>
      </ResponsiveContainer>

    </div>
  );
};

export default TopServiceRequestsChart;