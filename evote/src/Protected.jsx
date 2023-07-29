import React from "react";
import { Button, Result } from "antd";
import { getCookie } from "./lib/cookies";

const Protected = ({ children }) => {
  //Check for authCookie
  // if (!getCookie("evote_token")) {
  //   return <Unauthorized />;
  // }
  const validated = getCookie("voter_validated");
  const userId = getCookie("user_id");
  const pf = getCookie("pf_number");

  if (!validated || userId === "Guest" || !pf) {
    return <Unauthorized />;
  }
  // if (validated && userId !== "Guest") {
  //   navigate("/ballot");
  // }
  return <>{children}</>;
};
const Unauthorized = () => {
  const routeToLogin = () => {
    window.location.href = "/evote/login";
  };
  return (
    <Result
      status="403"
      title="Access Denied"
      subTitle="Sorry, you are not authorized to access this page, please login to gain access."
      extra={
        <Button onClick={() => routeToLogin()} type="primary">
          Back To Login
        </Button>
      }
    />
  );
};

export default Protected;
