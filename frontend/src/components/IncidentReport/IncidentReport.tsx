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
    name: string,
    ageRange_id: number,
    sex: string,
    workExperienceRange_id: number,

    industryTypeLarge_id: number,
    industryTypeMedium_id: number,
    workType_id: number,
    threatType_id: number,
    threatLevel: number,
    date: Date,
    factory_id: number,
    checks: Map<string, boolean>,
    description: string
  ) => {
    try {
      const newWorker = {
        name: name,
        ageRange_id: ageRange_id,
        sex: sex,
        workExperienceRange_id: workExperienceRange_id,
      };
      const newWorkerResponse = await api.post("/workers", newWorker);
      const newWorkerId = newWorkerResponse.data.id;
      const newIncident = {
        worker_id: newWorkerId,
        industryTypeLarge_id: industryTypeLarge_id,
        industryTypeMedium_id: industryTypeMedium_id,
        threatType_id: threatType_id,
        threatLevel: threatLevel,
        workType_id: workType_id,
        checks: Array.from(checks.entries()),
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
