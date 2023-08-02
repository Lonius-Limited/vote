import React from "react";
import { eraseCookie, getCookie, storedElectionCookies } from "../lib/cookies";
import { useFrappeAuth } from "frappe-react-sdk";
import { LogoutOutlined } from "@ant-design/icons";
import { Button, Result } from "antd";
import { useNavigate } from "react-router-dom";

const Logout = () => {
  const { logout, isLoading, isValidating } = useFrappeAuth();
  const navigate = useNavigate();
  //if (getCookie("user_id") !== "Guest") {
  storedElectionCookies.forEach((cookie) => eraseCookie(cookie));
  logout();
  if (isValidating || isLoading) {
    return <p>Please wait as we log you out...</p>;
  } else {
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
  }
  //}
};

export default Logout;
