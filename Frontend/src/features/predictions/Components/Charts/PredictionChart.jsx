import "../../css/PredictionChart.css";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Area
} from "recharts";

const PredictionChart = ({ data }) => {

  // ✅ Enhance data with error + range
  const enhancedData = data.map(item => {
    const error = Math.abs(item.actual - item.predicted);
    const errorPercent = ((error / item.actual) * 100).toFixed(1);

    return {
      ...item,
      error,
      errorPercent,
      upper: Math.max(item.actual, item.predicted),
      lower: Math.min(item.actual, item.predicted),
    };
  });

  // ✅ Custom Tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const d = payload[0].payload;

      return (
        <div style={{
          background: "#fff",
          padding: "10px",
          borderRadius: "8px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
          fontSize: "13px"
        }}>
          <strong>{label}</strong>
          <p>Actual: {d.actual}</p>
          <p>Predicted: {d.predicted}</p>
          <p style={{ color: d.error > 100 ? "#dc2626" : "#16a34a" }}>
            Error: {d.error} ({d.errorPercent}%)
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-wrapper">

      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={enhancedData}>

          <CartesianGrid stroke="#e5e7eb" />

          <XAxis dataKey="month" />
          <YAxis />

          <Tooltip content={<CustomTooltip />} />
          <Legend />

          {/* ✅ ERROR SHADING */}
          <Area
            type="monotone"
            dataKey="upper"
            stroke="none"
            fill="#93c5fd"
            fillOpacity={0.2}
          />
          <Area
            type="monotone"
            dataKey="lower"
            stroke="none"
            fill="#ffffff"
            fillOpacity={1}
          />

          {/* ACTUAL */}
          <Line
            type="monotone"
            dataKey="actual"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ r: 4 }}
          />

          {/* PREDICTED */}
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="#9ca3af"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ r: 4 }}
          />

        </LineChart>
      </ResponsiveContainer>

    </div>
  );
};

export default PredictionChart;