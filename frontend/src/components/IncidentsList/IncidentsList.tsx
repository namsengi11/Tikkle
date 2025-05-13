import Incident from "../Incident/Incident";
import { Incident as IncidentModel } from "../../models/Incident";
import "./IncidentsList.css";

const IncidentsList = ({ incidents }: { incidents: IncidentModel[] }) => {
  return (
    <ul className="incidentsScrollList">
      {incidents.map((incident: IncidentModel) => (
        <Incident key={incident.id} incident={incident} />
      ))}
    </ul>
  );
};

export default IncidentsList;
