import React, { useState } from "react";
import "./DropdownSelect.css";

interface DropdownOption {
  id: number;
  name: string;
}

interface DropdownSelectProps {
  options: DropdownOption[];
  onChange: (selectedId: number) => void;
  placeholder?: string;
  required?: boolean;
  id?: string;
}

const DropdownSelect = ({
  options,
  onChange,
  placeholder = "Select an option",
  required = false,
  id = "",
}: DropdownSelectProps) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setValue(parseInt(e.target.value));
    onChange(parseInt(e.target.value));
  };

  const [value, setValue] = useState<number>(-1);

  return (
    <div className="selectContainer">
      <select
        id={id}
        className="formInput"
        value={value === -1 ? "" : value}
        onChange={handleChange}
        required={required}
      >
        {/* Hidden option for placeholder - not visible in dropdown */}
        <option value="" disabled hidden>
          {placeholder}
        </option>
        {options.map((option) => (
          <option key={option.id} value={option.id}>
            {option.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default DropdownSelect;
