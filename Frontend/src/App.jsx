import Layout from "./features/predictions/Components/Layout/Layout";
import { Routes, Route } from "react-router-dom";

import PredictionDashboard from "./features/predictions/Pages/PredictionDashboard";
import CallCodeBifurcation from "./features/Call_code_page/pages/CallCodeBifurcation";

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<PredictionDashboard />} />
        <Route path="/predictions" element={<PredictionDashboard />} />
        <Route path="/bifurcation" element={<CallCodeBifurcation />} />

        <Route path="/incident" element={<h2>Incident Page</h2>} />
        <Route path="/service" element={<h2>Service Page</h2>} />
      </Routes>
    </Layout>
  );
}

export default App;