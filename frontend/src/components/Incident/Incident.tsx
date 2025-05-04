import React from "react";
import { format } from "date-fns";
import "./Incident.css";

interface IncidentProps {
  key: number;
  title: string;
  description: string;
  date: Date;
  [key: string]: any; // forward compatibility
}

const Incident: React.FC<IncidentProps> = ({
  key,
  title,
  description,
  date,
  ...otherProps
}) => {
  const formattedDate = format(date, "MM/dd/yyyy");

  return (
    <div className="incidentContainer">
      <div style={{width: "100%"}}>
        <div className="incidentContainerRow">
          <div className="incidentHeader">
            <h3 className="incidentTitle">{title}</h3>
            <span className="incidentDate">{formattedDate}</span>
          </div>
        </div>
        <div className="incidentContainerRow">
          <p className="incidentDescription">{description}</p>
          <button className="incidentButton">
            승인
          </button>
          <button className="incidentButton">
            조회
          </button>
        </div>
      </div>
    </div>
  );
};

export default Incident;
