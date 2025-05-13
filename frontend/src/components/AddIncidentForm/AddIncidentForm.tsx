import React, { useState, useEffect } from "react";
import api from "../../api";
import { Factory } from "../../models/Factory";
import { Category } from "../../models/Category";
import DropdownSelect from "../DropdownSelect/DropdownSelect";
import TrueFalseToggle from "../TrueFalseToggle/TrueFalseToggle";

import "./AddIncidentForm.css";
import ImageUploader from "../ImageUploader/ImageUploader";

const AddIncidentForm = ({
  onAdd,
}: {
  onAdd: (
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
  const [workTypes, setWorkTypes] = useState<Category[]>([]);
  const [workType_id, setWorkTypeId] = useState<number>(-1);
  const [checks, setChecks] = useState(new Map<string, boolean | null>());
  const [name, setName] = useState<string>("");
  const [ageRange, setAgeRange] = useState<Category[]>([]);
  const [ageRange_id, setAgeRangeId] = useState<number>(-1);
  const [sex, setSex] = useState<string>("");
  const [workExperienceRange, setWorkExperienceRange] = useState<Category[]>(
    []
  );
  const [workExperienceRange_id, setWorkExperienceRangeId] =
    useState<number>(-1);
  const [industryTypeLarge, setIndustryTypeLarge] = useState<Category[]>([]);
  const [industryTypeLarge_id, setIndustryTypeLargeId] = useState<number>(-1);
  const [industryTypeMedium, setIndustryTypeMedium] = useState<Category[]>([]);
  const [industryTypeMedium_id, setIndustryTypeMediumId] = useState<number>(-1);
  const [description, setDescription] = useState("");
  const [date, setDate] = useState(new Date());
  const [factories, setFactories] = useState<Factory[]>([]);
  const [factory_id, setFactoryId] = useState<number>(-1);
  // List of selectable factories

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
      name,
      ageRange_id,
      sex,
      workExperienceRange_id,

      industryTypeLarge_id,
      industryTypeMedium_id,
      workType_id,
      threatType_id,
      threatLevel,
      date,
      factory_id,
      checksResponse,
      description
    );
    setThreatTypeId(-1);
    setThreatLevel(-1);
    setWorkTypeId(-1);
    setDescription("");
    setDate(new Date());
    setFactoryId(-1);
    setChecks(checks);
    setName("");
    setAgeRangeId(-1);
    setSex("");
    setWorkExperienceRangeId(-1);
    setIndustryTypeLargeId(-1);
    setIndustryTypeMediumId(-1);
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

      const fetchAgeRanges = async () => {
        try {
          const response = await api.get("/ageRanges");
          const ageRangeObjects = response.data.ageRanges.map(
            (item: any) => new Category(item.id, item.range)
          );
          setAgeRange(ageRangeObjects);
        } catch (error) {
          console.error("Error fetching age ranges:", error);
        }
      };

      const fetchWorkExperienceRanges = async () => {
        try {
          const response = await api.get("/workExperienceRanges");
          const workExperienceRangeObjects =
            response.data.workExperienceRanges.map(
              (item: any) => new Category(item.id, item.range)
            );
          setWorkExperienceRange(workExperienceRangeObjects);
        } catch (error) {
          console.error("Error fetching work experience ranges:", error);
        }
      };

      const fetchIndustryTypesLarge = async () => {
        try {
          const response = await api.get("/industryTypes/large");
          const industryTypeLargeObjects = response.data.industryTypeLarge.map(
            (item: any) => new Category(item.id, item.name)
          );
          setIndustryTypeLarge(industryTypeLargeObjects);
        } catch (error) {
          console.error("Error fetching large industry types:", error);
        }
      };

      const fetchIndustryTypesMedium = async () => {
        try {
          const response = await api.get("/industryTypes/medium");
          const industryTypeMediumObjects =
            response.data.industryTypeMedium.map(
              (item: any) => new Category(item.id, item.name)
            );
          setIndustryTypeMedium(industryTypeMediumObjects);
        } catch (error) {
          console.error("Error fetching medium industry types:", error);
        }
      };

      // Execute all requests concurrently, but handle errors independently
      await Promise.allSettled([
        fetchFactories(),
        fetchThreatTypes(),
        fetchWorkTypes(),
        fetchChecks(),
        fetchAgeRanges(),
        fetchWorkExperienceRanges(),
        fetchIndustryTypesLarge(),
        fetchIndustryTypesMedium(),
      ]);
    };
    fetchData();
  }, []);

  // Add a new useEffect to set the industry type large ID after data is loaded
  useEffect(() => {
    if (industryTypeLarge.length > 0) {
      setIndustryTypeLargeId(industryTypeLarge[0].id); // Only one industry type large
    }
  }, [industryTypeLarge]);

  return (
    <form onSubmit={handleSubmit} className="incidentForm">
      <div className="formGroup">
        <h3
          style={{ color: "black", paddingBottom: "10px", paddingLeft: "10px" }}
        >
          근로자 정보
        </h3>
        <label className="formLabel" htmlFor="name">
          이름
        </label>
        <input
          type="text"
          className="formInput"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="이름을 입력해주세요"
          required
        />
        <label className="formLabel" htmlFor="ageRange">
          나이
        </label>
        <DropdownSelect
          options={ageRange}
          id="ageRange"
          onChange={setAgeRangeId}
          placeholder="나이를 선택해주세요"
          required
        />
        <label className="formLabel" htmlFor="sex">
          성별
        </label>
        <DropdownSelect
          options={[
            { id: 1, name: "남" },
            { id: 2, name: "여" },
          ]}
          id="sex"
          onChange={(selectedId) => setSex(selectedId === 1 ? "남" : "여")}
          placeholder="성별을 선택해주세요"
          required
        />
        <label className="formLabel" htmlFor="workExperienceRange">
          업무 경력
        </label>
        <DropdownSelect
          options={workExperienceRange}
          id="workExperienceRange"
          onChange={setWorkExperienceRangeId}
          placeholder="업무 경력을 선택해주세요"
          required
        />
      </div>

      <div className="formGroup">
        <h3
          style={{ color: "black", paddingBottom: "10px", paddingLeft: "10px" }}
        >
          미세 산재 정보
        </h3>

        <label className="formLabel" htmlFor="industryTypeMedium">
          업종
        </label>
        <DropdownSelect
          options={industryTypeMedium}
          id="industryTypeMedium"
          onChange={setIndustryTypeMediumId}
          placeholder="업종을 선택해주세요"
          required
        />
        <label className="formLabel" htmlFor="workType">
          작업 종류
        </label>
        <DropdownSelect
          options={workTypes}
          id="workType"
          onChange={setWorkTypeId}
          placeholder="작업 종류를 선택해주세요"
          required
        />
        <label className="formLabel" htmlFor="threatType">
          위험 유형
        </label>
        <DropdownSelect
          options={threatTypes}
          id="threatType"
          onChange={setThreatTypeId}
          placeholder="위험 유형을 선택해주세요"
          required
        />
        <label className="formLabel" htmlFor="threatLevel">
          위험도
        </label>
        <DropdownSelect
          options={threatLevels}
          id="threatLevel"
          onChange={setThreatLevel}
          placeholder="위험도를 1-5 사이의 수치로 나타내주세요"
          required
        />
        <label className="formLabel" htmlFor="date">
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
        <label className="formLabel" htmlFor="factory">
          발생 공장
        </label>
        <DropdownSelect
          options={factories}
          id="factory"
          onChange={setFactoryId}
          placeholder="산재 발생 공장을 선택해주세요"
          required
        />
        <label className="formLabel" htmlFor="image">
          이미지 첨부
        </label>
        <ImageUploader />
      </div>
      <div className="formGroup">
        <h3
          style={{ color: "black", paddingBottom: "10px", paddingLeft: "10px" }}
        >
          확인 체크리스트
        </h3>
        {Array.from(checks.entries()).map(([key, value]) => (
          <div key={key} className="checkListGroup">
            <label className="formLabel" htmlFor={key}>
              {key}
            </label>
            <TrueFalseToggle
              key={key}
              id={key}
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
        <label className="formLabel" htmlFor="description">
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
