import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../../api";
import { Incident } from "../../models/Incident";

import "./IncidentDetail.css";
import { AxiosError } from "axios";

const IncidentDetail = () => {
  const { id } = useParams();
  const [incident, setIncident] = useState<Incident | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchIncident = async () => {
      try {
        const response = await api.get(`/incidents/${id}`);
        setIncident(Incident.fromJson(response.data));
      } catch (error) {
        if (error instanceof AxiosError && error.response?.status === 404) {
          // change to 404
          navigate("/incidents");
        }
      }
    };
    fetchIncident();
  }, [id]);

  return (
    <div className="container">
      <h1 className="title">미세산재 상세 보고</h1>
      {incident ? (
        <>
          <div className="ThreeQuarterContainer">
            <div className="PhotoContainer">
              <h2 className="subtitle">사진</h2>
              <div
                style={{
                  width: "100%",
                  height: "80%",
                  backgroundColor: "#FFF",
                  borderRadius: "10px",
                }}
              />
            </div>
            <div className="SpecificInformationContainer">
              <h2 className="subtitle">관련 정보</h2>
              <div className="InfoList">
                {incident.getRelatedInfoInString().map(([key, value]) => (
                  <div key={key}>
                    <h3>{key}</h3>
                    <p>{value}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="OneQuarterContainer">
            <div className="DetailsContainer">
              <h2 className="subtitle">상세 정보</h2>
              <p>{incident.description}</p>
            </div>
          </div>
        </>
      ) : (
        <div className="loadingBox">로딩중...</div>
      )}
    </div>
  );
};

export default IncidentDetail;
