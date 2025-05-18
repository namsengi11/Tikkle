import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import IncidentReport from "./components/IncidentReport/IncidentReport";
import IncidentStatus from "./components/IncidentStatus/IncidentStatus";
import IncidentDetail from "./components/IncidentDetail/IncidentDetail";
import Navigation from "./components/Navigation/Navigation";
import Dashboard from "./components/Dashboard/Dashboard";
import ProfilePage from "./components/Profile/Profile";
import Login from "./components/Login/Login";
import Signup from "./components/Signup/Signup";

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <div className="App-content">
          <header className="App-header">
            <img
              src="/logo.png"
              alt="Tikkle Logo"
              style={{ height: "50px", marginRight: "10px" }}
            />
            <div className="loginStatus" style={{ marginLeft: "auto" }}>
              {localStorage.getItem("token") ? (
                <div className="userInfo">
                  <span>
                    {(() => {
                      try {
                        const token = localStorage.getItem("token");
                        if (!token) return "User";
                        const payload = JSON.parse(atob(token.split(".")[1]));
                        return payload.sub || "User";
                      } catch (e) {
                        return "User";
                      }
                    })()}
                  </span>
                  <button
                    onClick={() => {
                      localStorage.removeItem("token");
                      window.location.reload();
                    }}
                    style={{ marginLeft: "10px" }}
                  >
                    로그아웃
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => (window.location.href = "/login")}
                  className="loginButton"
                >
                  로그인
                </button>
              )}
            </div>
          </header>
          <main className="main">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/incidents" element={<IncidentStatus />} />
              <Route path="/incidents/report" element={<IncidentReport />} />
              <Route path="/incidents/:id" element={<IncidentDetail />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              {/* <Route path="*" element={<NotFound />} /> */}
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
