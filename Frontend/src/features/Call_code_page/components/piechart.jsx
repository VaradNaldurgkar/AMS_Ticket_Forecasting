import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import "../css/piechart.css";

const CALL_CODES = [
  "Chat",
  "E-Mail",
  "Personal",
  "Phone",
  "Transferred Request"
];

const COLORS = ["#2563eb", "#10b981", "#fb923c", "#ef4444", "#facc15"];

export default function CallCodePieChart({ data, title }) {
  const pieData = CALL_CODES.map(code => {
    const found = data.find(d => d.callCode === code);
    return {
      name: code,
      value: found ? found.percentage : 0
    };
  });

  return (
    <div className="pie-wrapper">
      <div className="pie-title">{title}</div>

      <ResponsiveContainer width="100%" height={240}>
        <PieChart>
          <Pie
            data={pieData}
            dataKey="value"
            innerRadius={60}
            outerRadius={90}
            label
          >
            {pieData.map((_, i) => (
              <Cell key={i} fill={COLORS[i]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}