import { useState } from "react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import "../../css/Layout.css";

const Layout = ({ children }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSidebar = () => setIsOpen(!isOpen);

  return (
    <div>
      <Navbar toggleSidebar={toggleSidebar} />
      <Sidebar isOpen={isOpen} />

      {isOpen && <div className="overlay" onClick={toggleSidebar}></div>}

      <div className={`content ${isOpen ? "shift" : ""}`}>
        {children}
      </div>
    </div>
  );
};

export default Layout;