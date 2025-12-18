import React, { useState, useRef } from "react";
import "./VerifyCode.css";
import { useNavigate } from "react-router-dom";

export default function VerifyCode({ onVerify }) {
  const [code, setCode] = useState(["", "", "", "", "", ""]);
  const inputsRef = useRef([]);
  const navigate = useNavigate()

  const handleChange = (value, index) => {
    if (!/^[0-9]?$/.test(value)) return;

    const newCode = [...code];
    newCode[index] = value;
    setCode(newCode);

    if (value && index < 5) {
      inputsRef.current[index + 1].focus();
    }
  };

  const handleKeyDown = (e, index) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      inputsRef.current[index - 1].focus();
    }
  };

  const handleSubmit = () => {
    const finalCode = code.join("");
    if (finalCode.length !== 6) {
      alert("Vui lòng nhập đủ 6 số!");
      return;
    }
    onVerify(finalCode); // gọi API verify từ component cha
  };

  return (
    <div className="verify-container" onKeyDown={(e) => {
      console.log(e.keyCode)
      if(e.keyCode == 13) navigate("/")
    }}>
      <h2 className="verify-title">Xác minh Email</h2>
      <p className="verify-subtitle">
        Vui lòng nhập mã xác nhận gồm 6 chữ số đã được gửi vào email của bạn.
      </p>

      <div className="otp-wrapper">
        {code.map((digit, index) => (
          <input
            key={index}
            type="text"
            maxLength="1"
            className="otp-box"
            value={digit}
            ref={(el) => (inputsRef.current[index] = el)}
            onChange={(e) => handleChange(e.target.value, index)}
            onKeyDown={(e) => handleKeyDown(e, index)}
          />
        ))}
      </div>

      <button className="btn-verify" onClick={handleSubmit}>
        Xác nhận
      </button>
    </div>
  );
}
