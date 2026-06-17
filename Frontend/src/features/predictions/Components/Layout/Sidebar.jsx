import "../../css/Sidebar.css";

import {
  FaChartLine,
  FaExclamationTriangle,
  FaServicestack,
  FaCodeBranch,
  FaUsers,
  FaUserCog,
  FaFileExcel
} from "react-icons/fa";

import { Link } from "react-router-dom";

const Sidebar = ({ isOpen }) => {
  return (
    <div className={`sidebar ${isOpen ? "open" : ""}`}>
      <ul className="sidebar-menu">

        <Link to="/predictions" className="menu-link">
          <li className="menu-item">
            <FaChartLine className="icon" />
            <span>Predictions</span>
          </li>
        </Link>

        <Link to="/incident" className="menu-link">
          <li className="menu-item">
            <FaExclamationTriangle className="icon" />
            <span>Incident Request</span>
          </li>
        </Link>

        <Link to="/service" className="menu-link">
          <li className="menu-item">
            <FaServicestack className="icon" />
            <span>Service Request</span>
          </li>
        </Link>

        <Link to="/bifurcation" className="menu-link">
          <li className="menu-item">
            <FaCodeBranch className="icon" />
            <span>Call Code Bifurcation</span>
          </li>
        </Link>

        <Link to="/fte-analysis" className="menu-link">
          <li className="menu-item">
            <FaUsers className="icon" />
            <span>FTE Analysis</span>
          </li>
        </Link>

        <Link to="/engineers" className="menu-link">
          <li className="menu-item">
            <FaUserCog className="icon" />
            <span>Engineers</span>
          </li>
        </Link>

        {/* New Add Excel Menu */}
        <Link to="/add-excel" className="menu-link">
          <li className="menu-item">
            <FaFileExcel className="icon" />
            <span>Add Excel</span>
          </li>
        </Link>

      </ul>
    </div>
  );
};

export default Sidebar;