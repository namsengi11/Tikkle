import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import IncidentReport from "./components/IncidentReport/IncidentReport";
import IncidentStatus from "./components/IncidentStatus/IncidentStatus";
import Navigation from "./components/Navigation/Navigation";
import Dashboard from "./components/Dashboard/Dashboard";

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <div className="App-content">
          <header className="App-header">
            <h1>티끌</h1>
          </header>
          <main className="main">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/incidents" element={<IncidentStatus />} />
              <Route path="/incidents/report" element={<IncidentReport />} />
              {/* <Route path="/incidents/:id" element={<IncidentDetail />} /> */}
              {/* <Route path="*" element={<NotFound />} /> */}
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
