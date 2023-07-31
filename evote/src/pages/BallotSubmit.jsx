import React from "react";
import { useContext } from "react";
import BallotContext from "../BallotContext";
import {
  useFrappeAuth,
  useFrappeGetCall,
  useFrappePostCall,
  useFrappePutCall,
} from "frappe-react-sdk";
import { Button, Result } from "antd";
import { useLocation } from "react-router-dom";

const BallotSubmit = () => {
  const location = useLocation();
  return (
    <>
      
      <div style={{ width: "90%", minWidth: "90%" }}>
        {/* {JSON.stringify(location)} */}
        <Result
          status="success"
          title={`Successfully Posted Your Ballot. Ref: ${location.state.ballotResult.message.name || ""}`}
          subTitle={`You will receive this reference in the Ballot Receipt SMS as a confirmation of your secured vote.`}
          extra={[
            <Button type="primary" key="buy" onClick={()=>window.location.href="/evote/stats"}>View Election Stats</Button>,
            <Button  key="console" onClick={()=>window.location.href="/evote/logout"}>
              Log Out
            </Button>,
            
          ]}
        />
      </div>
    </>
  );
};

export default BallotSubmit;
