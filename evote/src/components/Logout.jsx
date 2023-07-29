import React from "react";
import { eraseCookie, storedElectionCookies } from "../lib/cookies";
import { useFrappeAuth } from "frappe-react-sdk";
import { LogoutOutlined } from "@ant-design/icons";
import { Button, Result } from "antd";
import { useNavigate } from "react-router-dom";

const Logout = () => {
  const { logout, currentUser } = useFrappeAuth();
  const navigate = useNavigate();
  if (currentUser !== "Guest") {
    logout();
  }
  storedElectionCookies.forEach((cookie) => eraseCookie(cookie));
  return (
    <Result
      icon={<LogoutOutlined />}
      title={`Congratulations, You are logged out now!`}
      extra={
        <Button type="primary" onClick={() => navigate("/login")}>
          Go to Login
        </Button>
      }
    />
  );
};

export default Logout;
