import { useState, useRef, useEffect } from "react";
import axios from "axios";

import KPICard from "../components/KPICard";
import CallCodePieChart from "../components/piechart";
import CallCodeBarChart from "../components/barchart";
import InsightCard from "../components/InsightCard";
import ChannelBreakdown from "../components/ChannelBreakdown";
import QuickStats from "../components/QuickStats";

import "../css/CallCodeBifurcation.css";

export default function CallCodeBifurcation() {
  const ALL_OPTION = "All Issues";

  const [callCodeData, setCallCodeData] = useState([]);
  const [serviceData, setServiceData] = useState([]);

  const [selectedCategory, setSelectedCategory] = useState(ALL_OPTION);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  // ✅ FETCH DATA
  useEffect(() => {
    // INCIDENT
    axios.get("http://127.0.0.1:8000/api/call-code/incident")
      .then((res) => {
        const formatted = res.data.map((item) => ({
          callCode: item["Call Code"],
          category: item["Category"],
          count: item["Count"],
          percentage: item["Percentage"],
        }));
        setCallCodeData(formatted);
      })
      .catch(err => console.error("Incident API ERROR:", err));

    // SERVICE
    axios.get("http://127.0.0.1:8000/api/call-code/service")
      .then((res) => {
        const formatted = res.data.map((item) => ({
          callCode: item["Call Code"],
          category: item["Category"],
          count: item["Count"],
          percentage: item["Percentage"],
        }));
        setServiceData(formatted);
      })
      .catch(err => console.error("Service API ERROR:", err));

  }, []);

  // DROPDOWN
  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // CATEGORIES
  const categories = [
    ALL_OPTION,
    ...new Set(callCodeData.map((d) => d.category)),
  ];

  // FILTER
  const filterFn = (data) =>
    selectedCategory === ALL_OPTION
      ? Object.values(
          data.reduce((acc, d) => {
            if (!acc[d.callCode]) {
              acc[d.callCode] = { ...d, category: ALL_OPTION };
            } else {
              acc[d.callCode].count += d.count;
            }
            return acc;
          }, {})
        )
      : data.filter((d) => d.category === selectedCategory);

  const filteredData = filterFn(callCodeData);
  const filteredService = filterFn(serviceData);

  // ✅ 🔥 FIX: DYNAMIC BAR DATA (CATEGORY AWARE)
  const dynamicBarData = (() => {
    const map = {};

    // Incident
    filteredData.forEach((item) => {
      map[item.callCode] = {
        callCode: item.callCode,
        incident: item.count,
        service: 0,
      };
    });

    // Service
    filteredService.forEach((item) => {
      if (!map[item.callCode]) {
        map[item.callCode] = {
          callCode: item.callCode,
          incident: 0,
          service: item.count,
        };
      } else {
        map[item.callCode].service = item.count;
      }
    });

    return Object.values(map);
  })();

  // KPI
  const totalTickets = filteredData.reduce((s, d) => s + d.count, 0);

  const chatCount = filteredData
    .filter((d) => d.callCode === "Chat")
    .reduce((s, d) => s + d.count, 0);

  const chatShare =
    totalTickets > 0 ? Math.round((chatCount / totalTickets) * 100) : 0;

  const dominantChannel =
    filteredData.length > 0
      ? filteredData.reduce((max, d) =>
          d.count > max.count ? d : max
        ).callCode
      : "N/A";

  return (
    <div className="ccb-page">
      <h1 className="ccb-title">Call Code Bifurcation</h1>

      {/* DROPDOWN */}
      <div className="ccb-dropdown" ref={dropdownRef}>
        <button
          className="ccb-dropdown-trigger"
          onClick={() => setDropdownOpen((prev) => !prev)}
        >
          <span>{selectedCategory}</span>
          <svg
            className={`ccb-dropdown-chevron ${dropdownOpen ? "open" : ""}`}
            width="16"
            height="16"
            viewBox="0 0 24 24"
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </button>

        {dropdownOpen && (
          <ul className="ccb-dropdown-menu">
            {categories.map((cat) => (
              <li
                key={cat}
                className={`ccb-dropdown-item ${
                  cat === selectedCategory ? "active" : ""
                }`}
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

      {/* KPI */}
      <KPICard
        total={totalTickets}
        dominantChannel={dominantChannel}
        percentage={chatShare}
      />

      <div className="ccb-layout">
        <div className="ccb-main">

          {/* PIE */}
          <div className="ccb-pies-row">
            <div className="ccb-pie-box">
              <CallCodePieChart
                data={filteredData}
                title="Incident – Channel Distribution"
              />
            </div>

            <div className="ccb-pie-box">
              <CallCodePieChart
                data={filteredService}
                title="Service Request – Channel Distribution"
              />
            </div>
          </div>

          {/* ✅ BAR (NOW CHANGES WITH DROPDOWN) */}
          <div className="ccb-bar-box">
            <CallCodeBarChart data={dynamicBarData} />
          </div>
        </div>

        <div className="ccb-sidebar">
          <InsightCard
            title="Access Insight"
            heading="Channel Concentration Detected"
            description="Chat dominates nearly all tickets for this issue category."
            recommendation="Promote email fallback."
          />

          <ChannelBreakdown data={filteredData} />
          <QuickStats data={filteredData} totalTickets={totalTickets} />
        </div>
      </div>
    </div>
  );
}