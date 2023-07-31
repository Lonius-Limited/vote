import React from "react";
import {
  Button,
  Col,
  Input,
  Row,
  Statistic,
  message,
  Alert,
  Result,
} from "antd";
import { useParams } from "react-router-dom";
import { getCookie } from "../lib/cookies";
import { _defaultHeaders } from "../api/queries";
import { useFrappeGetCall } from "frappe-react-sdk";
import { useContext } from "react";
import BallotContext from "../BallotContext";
import ElectionSummary from "../components/ElectionSummary";
import BallotDetail from "../components/BallotDetail";
import BallotDetailV2 from "../components/BallotDetailV2";
const VotingPage = () => {
  //ballotReceipt, addToBallotReceipt

  const { election } = useParams();
  const { voter_id } = JSON.parse(getCookie("voter_registration_details"));
  const params = { election, voter: voter_id };
  const method = "vote.utils.election_details.get_e_ballot";
  const { data, error, isValidating, mutate } = useFrappeGetCall(
    method,
    params,
    _defaultHeaders
  );
  if (isValidating) {
    return (
      <Alert
        message="Please wait as we validate and your load your ballot page..."
        type="success"
      />
    );
  }
  if (error) {
    return (
      <>
        <Alert message={JSON.stringify(error)} type="error" />
        <Button type="link" onClick={() => window.location.reload()}>
          Try Again
        </Button>
      </>
    );
  }
  if (data) {
    if (data.message.has_voted === "Yes") {
      return <HasVoted />;
    }

    return (
      <div style={{ width: "100%" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {/* <ElectionSummary data={data.message} /> */}
          <BallotDetailV2 data={data.message} />
        </div>
      </div>
    );
  }
};
const HasVoted = () => (
  <Result
    status="404"
    // icon={<SmileOutlined />}
    title="Sorry, but you have voted already!"
    extra={[
      <Button
        type="primary"
        key="resultsbt"
        onClick={() => (window.location.href = "/evote/stats")}
      >
        Show Me Voting Statistics
      </Button>,
      <Button onClick={() => (window.location.href = "/evote/logout")}>
        Log Me Out
      </Button>,
    ]}
  />
);

export default VotingPage;
