import "../../css/Navbar.css";

const Navbar = ({ toggleSidebar }) => {
  return (
    <div className="navbar">
      <div className="hamburger" onClick={toggleSidebar}>
        ☰
      </div>

      <div className="title">
        AMS Ticket Forecasting
      </div>
    </div>
  );
};

export default Navbar;