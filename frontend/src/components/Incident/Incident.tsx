import React from "react";
import { format } from "date-fns";
import "./Incident.css";
import { Incident as IncidentModel } from "../../models/Incident";
import { useNavigate } from "react-router-dom";

interface IncidentProps {
  id?: number; // Optional id parameter
  incident: IncidentModel;
}

const Incident: React.FC<IncidentProps> = ({ incident, id }) => {
  const formattedDate = format(incident.date, "MM/dd/yyyy");
  const navigate = useNavigate();

  // Get risk level color based on threat level
  const getRiskLevelColor = (level: number) => {
    switch (level) {
      case 1:
        return "#4caf50"; // Low - Green
      case 2:
        return "#ff9800"; // Medium - Orange
      case 3:
        return "#f44336"; // High - Red
      default:
        return "#f44336"; // Default to red for unknown levels
    }
  };

  return (
    <div key={id} className="incidentContainer">
      <div className="incidentContent">
        <div className="incidentContainerRow">
          <div className="incidentHeader">
            <div className="incidentHeaderInfo">
              <h3 className="incidentTitle">
                {incident.workType.name} 작업 중 {incident.threatType.name}
              </h3>
              <p className="incidentFactoryName">{incident.factory.name}</p>
              <div
                className="incidentRiskLevel"
                style={{ color: getRiskLevelColor(incident.threatLevel) }}
              >
                Risk: {incident.threatLevel}
              </div>
            </div>
            <span className="incidentDate">{formattedDate}</span>
          </div>
        </div>
        <div className="incidentContainerRow">
          <div className="incidentDescriptionContainer">
            <p className="incidentDescription">{incident.description}</p>
            <p className="incidentWorker">작업자: {incident.worker.name}</p>
          </div>
          <button
            onClick={() => navigate(`/incidents/${incident.id}`)}
            className="incidentButton"
          >
            조회
          </button>
        </div>
      </div>
    </div>
  );
};

export default Incident;
