import React, { useState, useEffect } from "react";

import IncidentsList from "../IncidentsList/IncidentsList";
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
  // Loading states
  const [isLoadingFactories, setIsLoadingFactories] = useState<boolean>(true);
  const [isLoadingIncidents, setIsLoadingIncidents] = useState<boolean>(true);

  const handleFactoryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    // Clear incidents when factory changes
    setIncidents([]);

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
      try {
        const response: any = await api.get("/factories");
        const factoryObjects = response.data.factories.map(
          (item: any) => new Factory(item.id, item.name)
        );
        setFactories(factoryObjects);
        if (factoryObjects.length > 0) {
          setFactory(factoryObjects[0]);
        } else {
          setFactory(new Factory(-1, "No available factories"));
        }
      } catch (error) {
        console.error("Failed to fetch factories:", error);
        setFactories([]);
        setFactory(new Factory(-1, "Error loading factories"));
      } finally {
        setIsLoadingFactories(false);
      }
    };
    fetchFactories();
  }, []);

  useEffect(() => {
    const fetchIncidents = async () => {
      try {
        setIsLoadingIncidents(true);
        const response: any = await api.get(`/incidents/factory/${factory.id}`);
        const incidentObjects = response.data.incidents.map(
          (item: any) =>
            new Incident(
              item.id,
              item.worker,
              item.threatType,
              item.threatLevel,
              item.workType,
              item.checks,
              item.description,
              item.date,
              item.factory,
              item.additionalData
            )
        );
        setIncidents(incidentObjects);
      } catch (error) {
        console.error(
          `Failed to fetch incidents for factory ${factory.id}:`,
          error
        );
        setIncidents([]);
      } finally {
        setIsLoadingIncidents(false);
      }
    };
    if (factory.id !== -1) {
      fetchIncidents();
    }
  }, [factory]);

  return (
    <div className="container">
      {isLoadingFactories ? (
        <div className="loadingContainer">
          <p>로딩 중</p>
        </div>
      ) : (
        <div className="overview">
          {isLoadingIncidents ? (
            <h1 className="overviewTitle"></h1>
          ) : (
            <h1 className="overviewTitle">
              오늘 {factory.name} 에서는 총 {incidents.length}건의 위험요소가
              등록되었습니다.
            </h1>
          )}
          <div style={{ width: "25%", marginRight: "40px" }}>
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
        </div>
      )}
      <div className="incidentsList">
        <IncidentsList incidents={incidents} />
      </div>
    </div>
  );
};

export default IncidentStatus;
