import AddIncidentForm from "../AddIncidentForm/AddIncidentForm";
import api from "../../api";

const IncidentReport = () => {
  const addIncident = async (
    title: string,
    description: string,
    date: Date
  ) => {
    try {
      const newIncident = {
        title: title,
        description: description,
        date: date.toISOString(),
      };
      await api.post("/incidents", newIncident);
    } catch (error) {
      console.error("Error adding incident:", error);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flex: 1,
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <h1 style={{ margin: "20px", fontSize: "24px", fontWeight: "bold" }}>
        미세산재 신고
      </h1>
      <AddIncidentForm onAdd={addIncident} />
    </div>
  );
};

export default IncidentReport;
