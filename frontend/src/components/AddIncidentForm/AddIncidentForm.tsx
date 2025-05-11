import React, { useState, useEffect } from "react";
import api from "../../api";
import { Factory } from "../../models/Factory";
import { Category } from "../../models/Category";
import DropdownSelect from "../DropdownSelect/DropdownSelect";
import TrueFalseToggle from "../TrueFalseToggle/TrueFalseToggle";

import "./AddIncidentForm.css";

const AddIncidentForm = ({
  onAdd,
}: {
  onAdd: (
    threatType_id: number,
    threatLevel: number,
    workType_id: number,
    checks: Map<string, boolean>,
    description: string,
    date: Date,
    factory_id: number
  ) => void;
}) => {
  const [threatType_id, setThreatTypeId] = useState<number>(-1);
  const [threatTypes, setThreatTypes] = useState<any[]>([]);
  const [threatLevel, setThreatLevel] = useState<number>(-1);
  const threatLevels = [
    { id: 1, name: "1" },
    { id: 2, name: "2" },
    { id: 3, name: "3" },
    { id: 4, name: "4" },
    { id: 5, name: "5" },
  ];
  const [workType_id, setWorkTypeId] = useState<number>(-1);
  const [workTypes, setWorkTypes] = useState<any[]>([]);
  const [checks, setChecks] = useState(new Map<string, boolean | null>());
  const [description, setDescription] = useState("");
  const [date, setDate] = useState(new Date());
  const [factory_id, setFactoryId] = useState<number>(-1);
  // List of selectable factories
  const [factories, setFactories] = useState<Factory[]>([]);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // nullcheck all entries in checks
    const checksResponse: Map<string, boolean> = new Map();
    for (const [key, value] of checks.entries()) {
      if (value !== null) {
        checksResponse.set(key, value);
        checks.set(key, value);
      }
    }
    if (checksResponse.size !== checks.size) {
      alert("안전수칙 준수 여부를 모두 선택해주세요");
      return;
    }

    onAdd(
      threatType_id,
      threatLevel,
      workType_id,
      checksResponse,
      description,
      date,
      factory_id
    );
    setThreatTypeId(-1);
    setThreatLevel(-1);
    setWorkTypeId(-1);
    setDescription("");
    setDate(new Date());
    setFactoryId(-1);
    setChecks(checks);
  };

  useEffect(() => {
    const fetchData = async () => {
      // Create individual fetch functions with their own error handling
      const fetchFactories = async () => {
        try {
          const response = await api.get("/factories");
          const factoryObjects = response.data.factories.map(
            (item: any) => new Factory(item.id, item.name)
          );
          setFactories(factoryObjects);
        } catch (error) {
          console.error("Error fetching factories:", error);
          // You could set an error state here for factories specifically
        }
      };

      const fetchThreatTypes = async () => {
        try {
          const response = await api.get("/threatTypes");
          const threatTypeObjects = response.data.threatTypes.map(
            (item: any) => new Category(item.id, item.name)
          );
          setThreatTypes(threatTypeObjects);
        } catch (error) {
          console.error("Error fetching threat types:", error);
          // You could set an error state here for threat types specifically
        }
      };

      const fetchWorkTypes = async () => {
        try {
          const response = await api.get("/workTypes");
          const workTypeObjects = response.data.workTypes.map(
            (item: any) => new Category(item.id, item.name)
          );
          setWorkTypes(workTypeObjects);
        } catch (error) {
          console.error("Error fetching work types:", error);
          // You could set an error state here for work types specifically
        }
      };

      const fetchChecks = async () => {
        try {
          const response = await api.get("/checks");
          const checkObjects: Map<string, boolean | null> = new Map();
          for (const item of response.data.checks) {
            checkObjects.set(item.question, null);
          }
          setChecks(checkObjects);
        } catch (error) {
          console.error("Error fetching checks:", error);
        }
      };

      // Execute all requests concurrently, but handle errors independently
      await Promise.allSettled([
        fetchFactories(),
        fetchThreatTypes(),
        fetchWorkTypes(),
        fetchChecks(),
      ]);
    };

    fetchData();
  }, []);

  return (
    <form onSubmit={handleSubmit} className="incidentForm">
      <div className="formGroup">
        <label htmlFor="title" className="formLabel">
          위험 유형
        </label>
        <DropdownSelect
          options={threatTypes}
          onChange={setThreatTypeId}
          placeholder="위험 유형을 선택해주세요"
          required
        />
      </div>
      <div className="formGroup">
        <label htmlFor="title" className="formLabel">
          위험도
        </label>
        <DropdownSelect
          options={threatLevels}
          onChange={setThreatLevel}
          placeholder="위험도를 1-5 사이의 수치로 나타내주세요"
          required
        />
      </div>
      <div className="formGroup">
        <label htmlFor="date" className="formLabel">
          발생 일자
        </label>
        <input
          id="date"
          type="date"
          value={date.toISOString().split("T")[0]}
          onChange={(e) => setDate(new Date(e.target.value))}
          required={true}
          className="formInput"
        />
      </div>
      <div className="formGroup">
        <label htmlFor="factory" className="formLabel">
          발생 공장
        </label>
        <DropdownSelect
          options={factories}
          onChange={setFactoryId}
          placeholder="산재 발생 공장을 선택해주세요"
          required
        />
      </div>
      <div className="formGroup">
        <label htmlFor="title" className="formLabel">
          작업 종류
        </label>
        <DropdownSelect
          options={workTypes}
          onChange={setWorkTypeId}
          placeholder="작업 종류를 선택해주세요"
          required
        />
      </div>
      <div className="formGroup">
        <h3
          style={{ color: "black", paddingBottom: "10px", paddingLeft: "10px" }}
        >
          확인 체크리스트
        </h3>
        {Array.from(checks.entries()).map(([key, value]) => (
          <div className="formGroup">
            <label htmlFor={key} className="formLabel">
              {key}
            </label>
            <TrueFalseToggle
              key={key}
              initialValue={value}
              onChange={(newValue) => {
                const newChecks = new Map(checks);
                newChecks.set(key, newValue);
                setChecks(newChecks);
              }}
            />
          </div>
        ))}
      </div>

      <div className="formGroup">
        <label htmlFor="description" className="formLabel">
          상세 설명
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="미세산재에 대한 상세 설명을 입력해주세요"
          required
          className="formInput formTextarea"
        />
      </div>
      <button type="submit" className="submitButton">
        미세산재 신고
      </button>
    </form>
  );
};

export default AddIncidentForm;
