import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

const TopServiceRequestsChart = ({ data }) => {
  return (
    <div className="chart-card">

      <h2>Top Service Requests</h2>

      <BarChart
        width={520}
        height={300}
        data={data}
        layout="vertical"
        margin={{
          top: 5,
          right: 20,
          left: 60,
          bottom: 5,
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
          width={140}
        />

        <Tooltip />

        <Bar
          dataKey="tickets"
          fill="#00A76F"
          radius={[0, 6, 6, 0]}
        />

      </BarChart>

    </div>
  );
};

export default TopServiceRequestsChart;