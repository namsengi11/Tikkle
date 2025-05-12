import React, { useState } from "react";
import "./TrueFalseToggle.css";

interface TrueFalseToggleProps {
  initialValue?: boolean | null;
  onChange: (value: boolean | null) => void;
  id?: string;
}

const TrueFalseToggle: React.FC<TrueFalseToggleProps> = ({
  initialValue = null,
  onChange,
  id = "",
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

  // Add appropriate class based on selection state
  let containerClass = "trueFalseToggle";
  if (selectedValue === true) {
    containerClass += " trueSelected";
  } else if (selectedValue === false) {
    containerClass += " falseSelected";
  }

  return (
    <div className={containerClass} id={id}>
      <button
        className={`toggleButton ${selectedValue === true ? "selected" : ""}`}
        onClick={() => handleSelection(true)}
        aria-label="True"
        type="button"
      >
        <span className="checkmark">O</span>
      </button>
      <button
        className={`toggleButton ${selectedValue === false ? "selected" : ""}`}
        onClick={() => handleSelection(false)}
        aria-label="False"
        type="button"
      >
        <span className="xmark">X</span>
      </button>
    </div>
  );
};

export default TrueFalseToggle;
