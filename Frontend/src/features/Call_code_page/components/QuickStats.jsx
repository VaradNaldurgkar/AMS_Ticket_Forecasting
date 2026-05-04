import "../css/QuickStats.css";

export default function QuickStats({ data, totalTickets }) {
  const channelCount = [...new Set(data.map(d => d.callCode))].length;

  const chatCount = data
    .filter(d => d.callCode === "Chat")
    .reduce((s, d) => s + d.count, 0);

  const nonChatCount = totalTickets - chatCount;

  const dominanceScore = totalTickets > 0
    ? ((chatCount / totalTickets) * 100).toFixed(1)
    : 0;

  // Derived from data — top non-chat channel
  const nonChatChannels = data
    .filter(d => d.callCode !== "Chat")
    .sort((a, b) => b.count - a.count);

  const topAltChannel = nonChatChannels[0]?.callCode || "N/A";
  const topAltCount = nonChatChannels[0]?.count || 0;

  const emailCount = data
    .filter(d => d.callCode === "E-Mail")
    .reduce((s, d) => s + d.count, 0);

  const phoneCount = data
    .filter(d => d.callCode === "Phone")
    .reduce((s, d) => s + d.count, 0);

  const stats = [
    {
      label: "Active Channels",
      value: channelCount,
      sub: "in this category",
      color: "#0f766e",
    },
    {
      label: "Non-Chat Tickets",
      value: nonChatCount.toLocaleString(),
      sub: "via other channels",
      color: "#6366f1",
    },
    {
      label: "E-Mail Tickets",
      value: emailCount.toLocaleString(),
      sub: "email channel",
      color: "#dc2626",
    },
    {
      label: "Top Alt Channel",
      value: topAltChannel,
      sub: `${topAltCount} tickets`,
      color: "#16a34a",
    },
  ];

  return (
    <div className="qs-card">
      <div className="qs-header">
        <span className="qs-title">Quick Stats</span>
        <span className="qs-badge">{dominanceScore}% Chat</span>
      </div>

      <div className="qs-grid">
        {stats.map((s, i) => (
          <div className="qs-item" key={i}>
            <div className="qs-value" style={{ color: s.color }}>{s.value}</div>
            <div className="qs-label">{s.label}</div>
            <div className="qs-sub">{s.sub}</div>
          </div>
        ))}
      </div>
    </div>
  );
}