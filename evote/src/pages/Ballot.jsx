import React from "react";
import { useFrappeGetCall } from "frappe-react-sdk";
import { _defaultHeaders } from "../api/queries";
import { getCookie, setCookie } from "../lib/cookies";
import NoBallot from "../components/NoBallot";
import { useNavigate } from "react-router-dom";
const Ballot = () => {
  const navigate = useNavigate()
  const voterRegistration = getCookie("voter_registration_details");
  const status = "just_any";
  const { voter_id } = JSON.parse(voterRegistration);
  // console.log("vid",voterRegistration,voter_id)
  const params = { voter_id };
  const method = "vote.utils.election_details.get_voter_elections";
  const { data, error, isValidating } = useFrappeGetCall(
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
    const scheduledOROpen =
      data.message.find((x) => ["Scheduled", "Open"].includes(x.status)) || {};
      // data.message.find((x) => ["Closed"].includes(x.status)) || {};
    if (Object.keys(scheduledOROpen).length < 1) {
      return <NoBallot />;
    }
    setCookie("active_elections", JSON.stringify(scheduledOROpen), 12);

    // navigate(`/ballot/${scheduledOROpen.name}`)
    window.location.href = `/evote/ballot/${scheduledOROpen.name}`
  }
};

export default Ballot;
