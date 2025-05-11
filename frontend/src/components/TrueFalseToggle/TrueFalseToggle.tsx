import React, { useState } from "react";
import "./TrueFalseToggle.css";

interface TrueFalseToggleProps {
  initialValue?: boolean | null;
  onChange: (value: boolean | null) => void;
}

const TrueFalseToggle: React.FC<TrueFalseToggleProps> = ({
  initialValue = null,
  onChange,
}) => {
  const [selectedValue, setSelectedValue] = useState<boolean | null>(
    initialValue
  );

  const handleSelection = (value: boolean) => {
    // If the same value is clicked again, deselect it
    const newValue = selectedValue === value ? null : value;
    setSelectedValue(newValue);
    onChange(newValue);
  };

  return (
    <div className="trueFalseToggle">
      <button
        className={`toggleButton ${selectedValue === true ? "selected" : ""}`}
        onClick={() => handleSelection(true)}
        aria-label="True"
        type="button"
      >
        <span className="checkmark">✓</span>
      </button>
      <button
        className={`toggleButton ${selectedValue === false ? "selected" : ""}`}
        onClick={() => handleSelection(false)}
        aria-label="False"
        type="button"
      >
        <span className="xmark">✗</span>
      </button>
    </div>
  );
};

export default TrueFalseToggle;
