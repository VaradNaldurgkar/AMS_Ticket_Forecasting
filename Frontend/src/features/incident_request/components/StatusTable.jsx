import React, { useState } from "react";
import "../css/StatusTable.css";

const incidents = [
  { name: "Laptop", count: 441, status: "Open", trend: "up" },
  { name: "VPN", count: 352, status: "Closed", trend: "up" },
  { name: "Citrix", count: 270, status: "Pending", trend: "down" },
  { name: "Headset", count: 236, status: "Closed", trend: "neutral" },
  { name: "Laptop Issue", count: 203, status: "Open", trend: "up" },
  { name: "Access Issue", count: 170, status: "Pending", trend: "up" },
  { name: "MS Teams", count: 146, status: "Closed", trend: "down" },
  { name: "Any Application", count: 144, status: "Open", trend: "neutral" },
  { name: "Citrix Issue", count: 127, status: "Pending", trend: "up" },
  { name: "Internet", count: 117, status: "Closed", trend: "down" },
  { name: "Headset Issue", count: 115, status: "Open", trend: "neutral" },
  { name: "VPN Issue", count: 107, status: "Pending", trend: "up" },
  { name: "Wi-Fi", count: 92, status: "Closed", trend: "down" },
  { name: "Mouse", count: 81, status: "Open", trend: "neutral" },
  { name: "Outlook", count: 71, status: "Pending", trend: "up" },
];

const STATUS_META = {
  Open:    { cls: "badge--open",    label: "Open" },
  Closed:  { cls: "badge--closed",  label: "Closed" },
  Pending: { cls: "badge--pending", label: "Pending" },
};

const TREND_META = {
  up:      { icon: "↑", cls: "trend--up" },
  down:    { icon: "↓", cls: "trend--down" },
  neutral: { icon: "—", cls: "trend--neutral" },
};

const StatusTable = () => {
  const [sortKey, setSortKey] = useState("count");
  const [sortDir, setSortDir] = useState("desc");

  const sorted = [...incidents].sort((a, b) => {
    if (sortKey === "count") return sortDir === "desc" ? b.count - a.count : a.count - b.count;
    if (sortKey === "name")  return sortDir === "desc" ? b.name.localeCompare(a.name) : a.name.localeCompare(b.name);
    return 0;
  });

  const toggleSort = (key) => {
    if (sortKey === key) setSortDir(d => d === "desc" ? "asc" : "desc");
    else { setSortKey(key); setSortDir("desc"); }
  };

  const chevron = (key) => sortKey === key ? (sortDir === "desc" ? " ↓" : " ↑") : "";

  return (
    <div className="status-table-card">
      <div className="status-table-card__header">
        <h3 className="status-table-card__title">Status Breakdown</h3>
        <span className="status-table-card__count">{incidents.length} types</span>
      </div>
      <div className="status-table-wrapper">
        <table className="status-table">
          <thead>
            <tr>
              <th className="sortable" onClick={() => toggleSort("name")}>Incident Type{chevron("name")}</th>
              <th className="sortable" onClick={() => toggleSort("count")}>Tickets{chevron("count")}</th>
              <th>Status</th>
              <th>Trend</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((row, i) => {
              const s = STATUS_META[row.status];
              const t = TREND_META[row.trend];
              return (
                <tr key={i} className="status-table__row">
                  <td className="status-table__name">{row.name}</td>
                  <td className="status-table__count">{row.count}</td>
                  <td><span className={`badge ${s.cls}`}>{s.label}</span></td>
                  <td><span className={`trend ${t.cls}`}>{t.icon}</span></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default StatusTable;