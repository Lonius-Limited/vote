import React from "react";
import { Button, Result } from "antd";
import { getCookie } from "./lib/cookies";

const Protected = ({ children }) => {
  //Check for authCookie
  // if (!getCookie("evote_token")) {
  //   return <Unauthorized />;
  // }
  return <>{ children }</>;
};
const Unauthorized = () => {
  const routeToLogin = () => {
    window.location.href = "/evote/login";
  };
  return (
    <Result
      status="403"
      title="403"
      subTitle="Sorry, you are not authorized to access this page."
      extra={
        <Button onClick={() => routeToLogin()} type="primary">
          Back To Login
        </Button>
      }
    />
  );
};

export default Protected;
