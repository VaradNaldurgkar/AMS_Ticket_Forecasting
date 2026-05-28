import Layout from "./features/predictions/Components/Layout/Layout";
import { Routes, Route } from "react-router-dom";

import PredictionDashboard from "./features/predictions/Pages/PredictionDashboard";

import CallCodeBifurcation from "./features/Call_code_page/pages/CallCodeBifurcation";

import ServiceDashboard from "./features/service_request/Pages/ServiceDashboard";

import IncidentDashboard from "./features/incident_request/pages/IncidentDashboard";

import EngineersDashboard from "./features/engineers/pages/EngineersDashboard";

function App() {
  return (
    <Layout>
      <Routes>

        <Route
          path="/"
          element={<PredictionDashboard />}
        />

        <Route
          path="/predictions"
          element={<PredictionDashboard />}
        />

        <Route
          path="/bifurcation"
          element={<CallCodeBifurcation />}
        />

        <Route
          path="/incident"
          element={<IncidentDashboard />}
        />

        <Route
          path="/service"
          element={<ServiceDashboard />}
        />


        <Route
          path="/engineers"
          element={<EngineersDashboard />}
        />

      </Routes>
    </Layout>
  );
}

export default App;