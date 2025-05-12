import React, { useState } from "react";
import "./Profile.css";

const ProfilePage = () => {
  const [location, setLocation] = useState("");
  const [position, setPosition] = useState("");
  const [team, setTeam] = useState("");
  const [mileage, setMileage] = useState(500);

  const percent = Math.min(mileage / 1000, 1) * 100;

  return (
    <div className="profile-container">
      <div className="profile-box">
        <h2>프로필</h2>
        <img
          src="/worker.png"
          alt="프로필"
          className="profile-image"
        />
        <select value={location} onChange={(e) => setLocation(e.target.value)}>
          <option value="">근무지</option>
          <option value="대전">대전</option>
          <option value="청주">청주</option>
          <option value="울산">울산</option>
        </select>
        <select value={position} onChange={(e) => setPosition(e.target.value)}>
          <option value="">직무</option>
          <option value="현장직">현장직</option>
          <option value="관리직">관리직</option>
        </select>
        <select value={team} onChange={(e) => setTeam(e.target.value)}>
          <option value="">부서</option>
          <option value="작업1팀">작업 1팀</option>
          <option value="작업2팀">작업 2팀</option>
          <option value="안전관리1팀">안전관리 1팀</option>
          <option value="안전관리2팀">안전관리 2팀</option>
        </select>
      </div>
      <div className="mileage-box">
        <h2>내 마일리지</h2>
        <div className="circle">
          <svg viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" className="bg" />
            <circle
              cx="50"
              cy="50"
              r="45"
              className="progress"
              style={{ strokeDashoffset: 282.6 - (282.6 * percent) / 100 }}
            />
            <text x="50%" y="50%" dominantBaseline="middle" textAnchor="middle" className="mileage-text">
              {mileage}
            </text>
          </svg>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
