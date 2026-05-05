import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

import "../css/barchart.css";

export default function CallCodeBarChart({ data }) {

  // ✅ USE DATA DIRECTLY — NO FAKE TRANSFORMATION
  const barData = data.map(d => ({
    channel: d.callCode,
    Incident: d.incident,
    Service: d.service
  }));

  return (
    <div className="bar-wrapper">
      <div className="bar-title">
        Incident vs Service Request by Channel
      </div>

      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={barData} barCategoryGap={24}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />

          {/* ✅ KEY FIX */}
          <XAxis dataKey="channel" />
          <YAxis />
          <Tooltip />
          <Legend />

          <Bar
            dataKey="Incident"
            fill="#2563eb"
            barSize={32}
            radius={[4, 4, 0, 0]}
          />

          <Bar
            dataKey="Service"
            fill="#10b981"
            barSize={32}
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}