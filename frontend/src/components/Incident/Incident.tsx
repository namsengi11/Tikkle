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
      <div className="incidentHeader">
        <h3 className="incidentTitle">{title}</h3>
        <span className="incidentDate">{formattedDate}</span>
      </div>
      <p className="incidentDescription">{description}</p>
    </div>
  );
};

export default Incident;
