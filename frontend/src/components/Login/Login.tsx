import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import "./Login.css";
import api from "../../api";

interface LoginProps {
  onLogin?: (username: string, password: string) => Promise<void>;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const validateForm = () => {
    if (!username || !password) {
      setError("아이디와 비밀번호를 입력해주세요.");
      return false;
    }
    setError("");
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      if (!validateForm()) {
        return;
      }
      setIsLoading(true);

      const formDetails = new URLSearchParams();
      formDetails.append("username", username);
      formDetails.append("password", password);

      // Send request to API to get JWT token
      const response = await api.post("auth/token", formDetails);

      if (response.status !== 200) {
        throw new Error("Authentication failed");
      }

      const data = response.data;

      // Save the token to localStorage
      localStorage.setItem("token", data.access_token);

      // Call the onLogin callback if provided
      if (onLogin) {
        await onLogin(username, password);
      }

      navigate("/"); // Redirect to dashboard after successful login
      // Rerender the page
      window.location.reload();
    } catch (err) {
      setError("아이디 또는 비밀번호가 일치하지 않습니다.");
      console.error("Login error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="authContainer">
      <div className="authCard">
        <h2 className="authTitle">로그인</h2>

        {error && <div className="errorMessage">{error}</div>}

        <form onSubmit={handleSubmit} style={{ width: "25%" }}>
          <div className="loginFormGroup">
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="아이디"
              required
              className="authInput"
            />
          </div>

          <div className="loginFormGroup">
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="비밀번호"
              required
              className="authInput"
            />
          </div>

          <button type="submit" className="authButton" disabled={isLoading}>
            {isLoading ? "로그인 중..." : "로그인"}
          </button>
        </form>

        {/* <div className="authDivider">
          <span>OR</span>
        </div> */}

        {/* <div className="socialButtons">
          <button className="socialButton googleButton">
            <span className="socialIcon">G</span>
            Continue with Google
          </button>

          <button className="socialButton microsoftButton">
            <span className="socialIcon">M</span>
            Continue with Microsoft Account
          </button>

          <button className="socialButton appleButton">
            <span className="socialIcon">A</span>
            Continue with Apple
          </button>
        </div> */}

        <div className="authLinks">
          <p>
            계정이 없으신가요? <a href="/signup">회원가입</a>
          </p>
        </div>

        {/* <div className="authFooter">
          <a href="/terms">Terms of Use</a>
          <span className="divider">|</span>
          <a href="/privacy">Privacy Policy</a>
        </div> */}
      </div>
    </div>
  );
};

export default Login;
