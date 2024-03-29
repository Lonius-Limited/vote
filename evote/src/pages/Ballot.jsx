import React from "react";
import { useFrappeGetCall } from "frappe-react-sdk";
import { _defaultHeaders } from "../api/queries";
import { getCookie, setCookie } from "../lib/cookies";
import NoBallot from "../components/NoBallot";
import { useNavigate } from "react-router-dom";
import { Button, Result, Statistic } from "antd";
import { LoadingOutlined } from "@ant-design/icons";
const { Countdown } = Statistic;

const Ballot = () => {
  const navigate = useNavigate();
  const voterRegistration = getCookie("voter_registration_details");
  const status = "just_any";
  const { voter_id } = JSON.parse(voterRegistration);
  // console.log("vid",voterRegistration,voter_id)

  const swrOptions = { refreshInterval: 15000 };

  const params = { voter_id, status }; //status to be added , status
  const method = "vote.utils.election_details.get_voter_elections";
  const { data, error, isValidating } = useFrappeGetCall(
    method,
    params,
    _defaultHeaders,
    swrOptions
  );
  if (isValidating) {
    return <>Loading</>;
  }
  if (error) {
    return <>{JSON.stringify(error)}</>;
  }
  if (data) {
    const scheduledOROpen =
      data.message.filter((x) => ["Scheduled", "Open"].includes(x.status)) ||
      [];
    // data.message.find((x) => ["Closed"].includes(x.status)) || {};
    if (scheduledOROpen.length < 1) {
      return <NoBallot />;
    }
    const open = scheduledOROpen.find((x) => ["Open"].includes(x.status));
    const scheduled = scheduledOROpen.find((x) =>
      ["Scheduled"].includes(x.status)
    );

    if (scheduled) {
      return <ScheduledElectionTimer election={scheduled} />;
    }
    if (open) {
      setCookie("active_elections", JSON.stringify(open), 12);

      window.location.href = `/evote/ballot/${open.name}`;
    }
  }
};
const ScheduledElectionTimer = ({ election }) => {
  const { election_start, name } = election;
  const deadline = new Date(election_start);
  return (
    <>
      <Result
        
        icon={<LoadingOutlined />}
        title={
          <Countdown
            title={`There is an upcoming election on ${deadline.toDateString()}`}
            value={deadline}
            format="D day H hour m : s "
          />
        }
        extra={[
          <Button
            type="primary"
            key="resultsbt1"
            onClick={() => (window.location.href = `/evote/stats/${name}`)}
            block
          >
            Show Me Preliminary Statistics
          </Button>,
          <Button onClick={() => (window.location.href = "/evote/logout")} block>
            Log Me Out
          </Button>,
        ]}
      />
    </>
  );
};
export default Ballot;
