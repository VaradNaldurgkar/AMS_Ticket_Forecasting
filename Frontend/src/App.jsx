import Layout from "./components/layout/Layout";
import { Routes, Route } from "react-router-dom";
import PredictionDashboard from "./pages/PredictionDashboard";
import CallCodeBifurcation from "./Call_code_page/pages/CallCodeBifurcation";


function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<PredictionDashboard />} />
        <Route path="/predictions" element={<PredictionDashboard />} />
        <Route path="/bifurcation" element={<CallCodeBifurcation />} />


        {/* Temporary placeholders for now */}
        <Route path="/incident" element={<h2>Incident Page</h2>} />
        <Route path="/service" element={<h2>Service Page</h2>} />
      </Routes>
    </Layout>
  );
}

export default App;