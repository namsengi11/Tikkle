import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import "../Login/Login.css";
import api from "../../api";

interface SignupProps {
  onSignup?: (username: string, password: string) => Promise<void>;
}

const Signup: React.FC<SignupProps> = ({ onSignup }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const validateForm = () => {
    if (!username || !password || !confirmPassword) {
      setError("모든 정보를 입력해주세요.");
      return false;
    }

    if (password !== confirmPassword) {
      setError("비밀번호가 일치하지 않습니다.");
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!validateForm()) {
      return;
    }

    try {
      setIsLoading(true);

      // Send request to API to create account
      const response = await api.post("/auth/user", {
        username: username,
        password: password,
      });

      if (response.status !== 201) {
        throw new Error("회원가입에 실패했습니다.");
      }

      const formDetails = new URLSearchParams();
      formDetails.append("username", username);
      formDetails.append("password", password);

      // After successful signup, get token
      const tokenResponse = await api.post("/auth/token", formDetails);

      if (tokenResponse.status !== 200) {
        throw new Error("로그인에 실패했습니다.");
      }

      const data = tokenResponse.data;

      // Save the token to localStorage
      localStorage.setItem("token", data.access_token);

      // Call the onSignup callback if provided
      if (onSignup) {
        await onSignup(username, password);
      }

      navigate("/"); // Redirect to dashboard after successful signup
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError(
          "계정 생성에 실패했습니다. 이미 사용중인 아이디일 수 있습니다."
        );
      }
      console.error("Signup error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="authContainer">
      <div className="authCard">
        <h2 className="authTitle">회원가입</h2>

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

          <div className="loginFormGroup">
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="비밀번호 확인"
              required
              className="authInput"
            />
          </div>

          <button type="submit" className="authButton" disabled={isLoading}>
            {isLoading ? "회원가입 중..." : "회원가입"}
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
            이미 계정이 있으신가요? <a href="/login">로그인</a>
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

export default Signup;
