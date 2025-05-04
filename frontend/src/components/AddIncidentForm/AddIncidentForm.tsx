import React, { useState, useEffect } from "react";
import api from "../../api";
import { Factory } from "../../models/Factory";

import "./AddIncidentForm.css";

const AddIncidentForm = ({
  onAdd,
}: {
  onAdd: (
    title: string,
    description: string,
    date: Date,
    factory_id: number
  ) => void;
}) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [date, setDate] = useState(new Date());
  const [factory_id, setFactoryId] = useState<number>(-1);
  // List of selectable factories
  const [factories, setFactories] = useState<Factory[]>([]);
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (title && description && date) {
      onAdd(title, description, date, factory_id);
      setTitle("");
      setDescription("");
      setDate(new Date());
      setFactoryId(factories[0].id);
    }
  };

  useEffect(() => {
    const fetchFactories = async () => {
      const response: any = await api.get("/factories");
      const factoryObjects = response.data.factories.map(
        (item: any) => new Factory(item.id, item.name)
      );
      setFactories(factoryObjects);
      try {
        setFactoryId(factoryObjects[0].id);
      } catch (error) {
        console.error("Empty factory list fetched", error);
      }
    };
    fetchFactories();
  }, []);

  return (
    <form onSubmit={handleSubmit} className="incidentForm">
      <div className="formGroup">
        <label htmlFor="title" className="formLabel">
          미세산재
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="미세산재 요약 (예: 10m 높이에서 자재 추락)"
          required
          className="formInput"
        />
      </div>
      <div className="formGroup">
        <label htmlFor="description" className="formLabel">
          상세 설명
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="미세산재 상세 설명"
          required
          className="formInput formTextarea"
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
          required
          className="formInput"
        />
      </div>
      <div className="formGroup">
        <label htmlFor="factory" className="formLabel">
          발생 공장
        </label>
        <select
          id="factory"
          className="formInput"
          onChange={(e) => setFactoryId(parseInt(e.target.value))}
        >
          {factories.map((factory) => (
            <option key={factory.id} value={factory.id}>
              {factory.name}
            </option>
          ))}
        </select>
      </div>
      <button type="submit" className="submitButton">
        미세산재 신고
      </button>
    </form>
  );
};

export default AddIncidentForm;
