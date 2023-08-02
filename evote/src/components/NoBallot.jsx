import React from "react";
import { Button, Result } from "antd";
import { _defaultHeaders } from "../api/queries";
import { useNavigate } from "react-router-dom";

const NoBallot = () => {
  const navigate = useNavigate();
  return (
    <Result
      status="warning"
      title={` Dear voter, there are no open or scheduled elections for now. Please check at a later date`}
      extra={[
        <Button
          type="primary"
          key="stats"
          onClick={() => navigate("/stats")}
        >
          Show me previous election stats
        </Button>,
        <Button
          
          key="console"
          onClick={() => navigate("/logout")}
        >
          Log Me Out
        </Button>
      ]}
    />
  );
};
export default NoBallot;
