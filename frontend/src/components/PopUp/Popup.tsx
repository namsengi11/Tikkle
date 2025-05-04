import React from "react";
import "./Popup.css";

interface PopupProps {
  notification: {
    show: boolean;
    message: string;
    isSuccess: boolean;
  };
}

const Popup: React.FC<PopupProps> = ({ notification }) => {
  if (!notification.show) return null;

  return (
    <div className={`popup ${notification.isSuccess ? "success" : "error"}`}>
      {notification.message}
    </div>
  );
};

export default Popup;
