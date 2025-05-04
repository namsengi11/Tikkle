import React, { useState, useEffect } from "react";
import api from "../api";
import Incident from "./Incident/Incident";

const IncidentsList = () => {
  const [incidents, setIncidents] = useState([]);

  const fetchIncidents = async () => {
    try {
      const response = await api.get("/incidents");
      setIncidents(response.data.incidents);
    } catch (error) {
      console.error("Error fetching incidents:", error);
    }
  };

  useEffect(() => {
    fetchIncidents();
  }, []);

  return (
    <div>
      <ul>
        {incidents.map((incident: any) => (
          <Incident
            key={incident.id}
            title={incident.title}
            description={incident.description}
            date={incident.date}
          />
        ))}
      </ul>
    </div>
  );
};

export default IncidentsList;
