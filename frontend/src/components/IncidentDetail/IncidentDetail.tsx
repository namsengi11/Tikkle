import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../../api";
import { Incident } from "../../models/Incident";
import { Category } from "../../models/Category";

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
          <div className="DetailBoardContainer">
            <div className="leftContainer">
              <h2 className="subtitle">사진</h2>
              <div
                style={{
                  display: "flex",
                  width: "90%",
                  height: "80%",
                  borderRadius: "10px",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <img
                  src="/incident_collapse.jpg"
                  alt="incident_collapse"
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                    maxWidth: "90%",
                    maxHeight: "90%",
                  }}
                />
              </div>
              <div
                className="riskInfoContainer"
                style={{ width: "90%", height: "20%", flex: 1 }}
              >
                <h3 className="riskInfoTitle">산재 설명</h3>
                <p style={{ fontSize: "1.1rem" }}>{incident.description}</p>
              </div>
            </div>
            <div className="rightContainer">
              <h2 className="subtitle">관련 정보</h2>
              <div className="riskInfoContainer" style={{ flex: 1 }}>
                <div className="WorkerInformation">
                  <h3 style={{ fontSize: "1.2rem" }}>작업자</h3>
                  <div className="WorkerInformationItem">
                    <p
                      className="WorkerInformationText"
                      style={{ fontSize: "1.3rem" }}
                    >
                      이름: {incident.worker.name} / 성별: {incident.worker.sex}{" "}
                      / 연령대:{" "}
                      {Category.createFromRange(
                        incident.worker.ageRange
                      ).toString()}{" "}
                      / 경력:{" "}
                      {Category.createFromRange(
                        incident.worker.workExperienceRange
                      ).toString()}
                    </p>
                  </div>
                </div>
              </div>
              <div className="riskInfoContainer" style={{ flex: 2.5 }}>
                <h3 className="riskInfoTitle">위험 정보</h3>
                <div className="riskInfoGrid">
                  <div
                    style={{
                      width: "100%",
                      height: "50%",
                      display: "flex",
                      flexDirection: "row",
                      alignItems: "center",
                      justifyContent: "space-between",
                      paddingTop: "10px",
                      paddingBottom: "10px",
                    }}
                  >
                    <div className="riskInfoItem" style={{ width: "48%" }}>
                      <div className="riskInfoLabel">위험요소 종류</div>
                      <div className="riskInfoValue">
                        {incident.threatType.name}
                      </div>
                    </div>
                    <div className="riskInfoItem" style={{ width: "48%" }}>
                      <div className="riskInfoLabel">작업 종류</div>
                      <div className="riskInfoValue">
                        {incident.workType.name}
                      </div>
                    </div>
                  </div>
                  <div style={{ width: "100%", height: "50%" }}>
                    <div className="riskInfoItem">
                      <div className="riskInfoLabel">위험요소 레벨</div>
                      <div className="riskInfoValue">
                        <div className="riskLevelVisualizer">
                          <span className="riskLevelText">
                            {incident.threatLevel}
                          </span>
                          <div className="riskLevelBar">
                            {[1, 2, 3, 4, 5].map((level) => (
                              <div
                                key={level}
                                className={`riskLevelSegment ${
                                  level <= incident.threatLevel ? "active" : ""
                                } level-${level}`}
                              />
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="riskInfoContainer" style={{ flex: 1 }}>
                <h3
                  className="riskInfoTitle"
                  style={{ fontSize: "1.2rem", color: "black" }}
                >
                  발생 정보
                </h3>
                <div
                  style={{
                    display: "flex",
                    flexDirection: "row",
                    alignItems: "center",
                    justifyContent: "space-between",
                    width: "100%",
                    height: "100%",
                  }}
                >
                  <div className="riskInfoItem" style={{ width: "48%" }}>
                    <h3>발생 공장</h3>
                    <p>{incident.factory.name}</p>
                  </div>
                  <div className="riskInfoItem" style={{ width: "48%" }}>
                    <h3>발생 날짜</h3>
                    <p>{incident.date.toLocaleDateString()}</p>
                  </div>
                </div>
              </div>
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
