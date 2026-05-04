import { useState, useRef, useEffect } from "react";
import { callCodeData } from "../data/callcodedata";
import KPICard from "../components/KPICard";
import CallCodePieChart from "../components/piechart";
import CallCodeBarChart from "../components/barchart";
import InsightCard from "../components/InsightCard";
import ChannelBreakdown from "../components/ChannelBreakdown";
import QuickStats from "../components/QuickStats";
import "../css/CallCodeBifurcation.css";

export default function CallCodeBifurcation() {
  const ALL_OPTION = "All Issues";
  const categories = [ALL_OPTION, ...new Set(callCodeData.map(d => d.category))];
  const [selectedCategory, setSelectedCategory] = useState(ALL_OPTION);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // When "All Issues" is selected, aggregate counts across all categories by callCode
  const filteredData =
    selectedCategory === ALL_OPTION
      ? Object.values(
          callCodeData.reduce((acc, d) => {
            if (!acc[d.callCode]) {
              acc[d.callCode] = { ...d, category: ALL_OPTION };
            } else {
              acc[d.callCode].count += d.count;
            }
            return acc;
          }, {})
        )
      : callCodeData.filter(d => d.category === selectedCategory);
  const totalTickets = filteredData.reduce((s, d) => s + d.count, 0);

  // Fixed: d.callCode instead of d.channel
  const chatCount = filteredData
    .filter(d => d.callCode === "Chat")
    .reduce((s, d) => s + d.count, 0);
  const chatShare = totalTickets > 0 ? Math.round((chatCount / totalTickets) * 100) : 0;

  // Dynamic dominant channel instead of hardcoded "Chat"
  const dominantChannel = filteredData.reduce(
    (max, d) => (d.count > max.count ? d : max),
    filteredData[0]
  )?.callCode || "Chat";

  return (
    <div className="ccb-page">
      <h1 className="ccb-title">Call Code Bifurcation</h1>

      <div className="ccb-dropdown" ref={dropdownRef}>
        <button
          className="ccb-dropdown-trigger"
          onClick={() => setDropdownOpen(prev => !prev)}
        >
          <span>{selectedCategory}</span>
          <svg
            className={`ccb-dropdown-chevron ${dropdownOpen ? "open" : ""}`}
            width="16" height="16" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" strokeWidth="2"
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </button>

        {dropdownOpen && (
          <ul className="ccb-dropdown-menu">
            {categories.map(cat => (
              <li
                key={cat}
                className={`ccb-dropdown-item ${cat === selectedCategory ? "active" : ""}`}
                onClick={() => {
                  setSelectedCategory(cat);
                  setDropdownOpen(false);
                }}
              >
                {cat}
              </li>
            ))}
          </ul>
        )}
      </div>

      <KPICard
        total={totalTickets}
        dominantChannel={dominantChannel}
        percentage={chatShare}
      />

      <div className="ccb-layout">
        <div className="ccb-main">
          <div className="ccb-pies-row">
            <div className="ccb-pie-box">
              <CallCodePieChart
                data={filteredData}
                title="Incident – Channel Distribution"
              />
            </div>
            <div className="ccb-pie-box">
              <CallCodePieChart
                data={filteredData}
                title="Service Request – Channel Distribution"
              />
            </div>
          </div>
          <div className="ccb-bar-box">
            <CallCodeBarChart data={filteredData} />
          </div>
        </div>

        <div className="ccb-sidebar">
          <InsightCard
            title="Access Insight"
            heading="Channel Concentration Detected"
            description="Chat dominates nearly all tickets for this issue category, indicating heavy reliance on a single channel."
            recommendation="Promote email self-service as a fallback flow to reduce dependency risk."
          />
          <ChannelBreakdown data={filteredData} />
          <QuickStats data={filteredData} totalTickets={totalTickets} />
        </div>
      </div>
    </div>
  );
}