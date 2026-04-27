import "../../css/PredictionChart.css";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend, ResponsiveContainer
} from "recharts";

const PredictionChart = ({ data }) => {
  return (
    <div className="chart-wrapper">

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid stroke="#e5e7eb" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />

          <Line type="monotone" dataKey="actual" stroke="#2563eb" strokeWidth={2} />
          <Line type="monotone" dataKey="predicted" stroke="#9ca3af" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>

    </div>
  );
};

export default PredictionChart;