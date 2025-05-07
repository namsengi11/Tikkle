import Incident from "./Incident/Incident";
import { Incident as IncidentModel } from "../models/Incident";

const IncidentsList = ({ incidents }: { incidents: IncidentModel[] }) => {
  return (
    <div>
      <ul>
        {incidents.map((incident: IncidentModel) => (
          <Incident key={incident.id} incident={incident} />
        ))}
      </ul>
    </div>
  );
};

export default IncidentsList;
