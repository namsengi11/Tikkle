
import { NavLink, useLocation } from "react-router-dom";
import "./Navigation.css";

const Navigation = () => {
  const location = useLocation();

  return (
    <nav className="navigation">
      <ul>
        <li>
          <NavLink to="/" end>
            대시보드
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/incidents"
            className={({ isActive }) => {
              if (
                isActive &&
                location.pathname.startsWith("/incidents") &&
                !location.pathname.includes("/incidents/report")
              ) {
                return "active";
              } else {
                return "";
              }
            }}
          >
            미세산재 현황
          </NavLink>
        </li>
        <li>
          <NavLink to="/incidents/report" end>
            미세산재 신고
          </NavLink>
        </li>
        <li>
          <NavLink to="/profile" end>
            내 정보
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navigation;
