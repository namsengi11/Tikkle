import React, { useState, useEffect } from "react";

import IncidentsList from "../IncidentsList";
import api from "../../api";
import { Factory } from "../../models/Factory";
import { Incident } from "../../models/Incident";
import "./IncidentStatus.css";

const IncidentStatus = () => {
  // Choose current factory
  const [factory, setFactory] = useState<Factory>(
    new Factory(-1, "Placeholder")
  );
  // List of selectable factories
  const [factories, setFactories] = useState<Factory[]>([]);
  // List of incidents
  const [incidents, setIncidents] = useState<Incident[]>([]);

  const handleFactoryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    // Select from factories using selected value
    const selectedFactory = factories.find(
      (f) => f.id === parseInt(event.target.value)
    );
    if (selectedFactory) {
      setFactory(selectedFactory);
    }
  };

  useEffect(() => {
    const fetchFactories = async () => {
      const response: any = await api.get("/factories");
      const factoryObjects = response.data.factories.map(
        (item: any) => new Factory(item.id, item.name)
      );
      setFactories(factoryObjects);
      try {
        setFactory(factoryObjects[0]);
      } catch (error) {
        setFactory(new Factory(-1, "No available factories"));
        console.error("No available factories:", error);
      }
    };
    fetchFactories();
  }, []);

  useEffect(() => {
    const fetchIncidents = async () => {
      const response: any = await api.get(`/incidents/factory/${factory.id}`);
      const incidentObjects = response.data.incidents.map(
        (item: any) =>
          new Incident(
            item.id,
            item.title,
            item.description,
            item.date,
            item.factory_id
          )
      );
      setIncidents(incidentObjects);
      console.log(incidentObjects);
    };
    fetchIncidents();
  }, [factory]);

  return (
    <div className="container">
      <div className="overview">
        <h1 className="overviewTitle">
          오늘 {factory.name} 에서는 총 {incidents.length}건의 위험요소가
          등록되었습니다.
        </h1>
        <select
          value={factory.id}
          onChange={handleFactoryChange}
          className="factorySelect"
        >
          {factories.map((factory: Factory) => (
            <option key={factory.id} value={factory.id}>
              {factory.name}
            </option>
          ))}
        </select>
      </div>
      <div className="incidentsList">
        <IncidentsList />
      </div>
    </div>
  );
};

export default IncidentStatus;
