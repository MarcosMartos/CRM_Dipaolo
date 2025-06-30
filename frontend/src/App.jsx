// src/App.jsx
import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import DashboardLayout from "./pages/Dashboard";
import Metrics from "./pages/Metrics";
import Upload from "./pages/Upload";
import PrivateRoute from "./components/PrivateRoute";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <DashboardLayout />
          </PrivateRoute>
        }
      >
        <Route path="metrics" element={<Metrics />} />
        <Route path="upload" element={<Upload />} />
        <Route index element={<Metrics />} /> {/* Página por defecto */}
      </Route>
    </Routes>
  );
}

export default App;
