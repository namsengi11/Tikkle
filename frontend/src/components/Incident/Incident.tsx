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

  return (
    <div key={id} className="incidentContainer">
      <div style={{ width: "100%" }}>
        <div className="incidentContainerRow">
          <div className="incidentHeader">
            <h3 className="incidentTitle">{incident.threatType?.name}</h3>
            <span className="incidentDate">{formattedDate}</span>
          </div>
        </div>
        <div className="incidentContainerRow">
          <p className="incidentDescription">{incident.description}</p>
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
