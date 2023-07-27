import React from "react";
import BallotDetail from "../components/BallotDetail";
import ElectionSummary from "../components/ElectionSummary";
import { useFrappeGetCall } from "frappe-react-sdk";
//get_voter_elections
//get_e_ballot
const Ballot = () => {
  return (
    <div style={{ width: "100%" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
        <ElectionSummary />
      </div>
      <BallotDetail />
    </div>
  );
};

const TestPing = () => {
  const params = {};
  const method = "vote.utils.election_details.ping";
  const _defaultHeaders = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "X-Requested-With",
  };
  const { data, error, isValidating, mutate } = useFrappeGetCall(
    method,
    params,
    _defaultHeaders
  );
  if (isValidating) {
    return <>Loading</>;
  }
  if (error) {
    return <>{JSON.stringify(error)}</>;
  }
  if (data) {
    return <>{JSON.stringify(data)}</>;
  }
};

export default Ballot;
