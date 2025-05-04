import { useState } from "react";
import AddIncidentForm from "../AddIncidentForm/AddIncidentForm";
import api from "../../api";
import Popup from "../PopUp/Popup";

const IncidentReport = () => {
  const [notification, setNotification] = useState<{
    show: boolean;
    message: string;
    isSuccess: boolean;
  }>({ show: false, message: "", isSuccess: false });

  const addIncident = async (
    title: string,
    description: string,
    date: Date,
    factory_id: number
  ) => {
    try {
      const newIncident = {
        title: title,
        description: description,
        date: date.toISOString(),
        factory_id: factory_id,
      };
      await api.post("/incidents", newIncident);
      setNotification({
        show: true,
        message: "신고가 성공적으로 제출되었습니다.",
        isSuccess: true,
      });
      setTimeout(
        () => setNotification({ show: false, message: "", isSuccess: false }),
        5000
      );
    } catch (error) {
      console.error("Error adding incident:", error);
      setNotification({
        show: true,
        message: "신고 제출 중 오류가 발생했습니다.",
        isSuccess: false,
      });
      setTimeout(
        () => setNotification({ show: false, message: "", isSuccess: false }),
        5000
      );
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flex: 1,
        flexDirection: "column",
        alignItems: "center",
        position: "relative",
      }}
    >
      <Popup notification={notification} />
      <h1
        style={{
          margin: "20px",
          fontSize: "24px",
          fontWeight: "bold",
          color: "#333",
        }}
      >
        미세산재 신고
      </h1>
      <AddIncidentForm onAdd={addIncident} />
    </div>
  );
};

export default IncidentReport;
