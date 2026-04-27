import Layout from "./components/layout/Layout";
import { Routes, Route } from "react-router-dom";
import PredictionDashboard from "./pages/PredictionDashboard";

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<PredictionDashboard />} />
        <Route path="/predictions" element={<PredictionDashboard />} />

        {/* Temporary placeholders for now */}
        <Route path="/incident" element={<h2>Incident Page</h2>} />
        <Route path="/service" element={<h2>Service Page</h2>} />
        <Route path="/bifurcation" element={<h2>Bifurcation Page</h2>} />
      </Routes>
    </Layout>
  );
}

export default App;