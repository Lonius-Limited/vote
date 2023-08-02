import React from "react";
import { useFrappeGetCall } from "frappe-react-sdk";
import { _defaultHeaders } from "../api/queries";
import { getCookie, setCookie } from "../lib/cookies";
import { useNavigate } from "react-router-dom";
import { Button, Empty, List, Avatar } from "antd";

const Results = () => {
  const voterRegistration = getCookie("voter_registration_details");
  const status = "just_any";
  const { voter_id } = JSON.parse(voterRegistration);
  // console.log("vid",voterRegistration,voter_id)
  const params = { voter_id, status };
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
    const closedOROpen =
      data.message.filter((x) => ["Closed", "Open"].includes(x.status)) || [];
    // data.message.find((x) => ["Closed"].includes(x.status)) || {};
    if (closedOROpen.length < 1) {
      <Empty
        image="https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg"
        imageStyle={{
          height: 60,
        }}
        description={<span>No stats for now.</span>}
      >
        <Button
          type="primary"
          onClick={() => (window.location.href = "/evote/logout")}
        >
          Log Me Out
        </Button>
      </Empty>;
    }
    if (closedOROpen.length === 1) {
      setCookie("active_elections", JSON.stringify(closedOROpen[0].name), 12);
      window.location.href = `/evote/stats/${closedOROpen[0].name}`;
      return;
    }
    return (
      <div style={{ width: "90%", minWidth: "90%" }}>
        <RecentElections payload={closedOROpen} />;
      </div>
    );
    //

    // navigate(`/ballot/${scheduledOROpen.name}`)
    // window.location.href = `/evote/stats/${scheduledOROpen.name}`;
  }
};
const RecentElections = ({ payload }) => {
  return (
    <>
      <h2>No open election currently. Please select one of the elections below to view stats</h2>
      <List
        itemLayout="horizontal"
        dataSource={payload}
        renderItem={(item, index) => (
          <List.Item
          actions={[<Button type="primary" onClick={()=>window.location.href = `/evote/stats/${closedOROpen[0].name}`}>Open Stats</Button>]}
          >
            <List.Item.Meta
              avatar={
                <Avatar
                  style={{
                    backgroundColor: "#fde3cf",
                    color: "#f56a00",
                  }}
                >
                  ...
                </Avatar>
              }
              title={<a href={`/evote/stats/${item.name}`}>{item.name}</a>}
              description={`${item.election_start} - ${item.election_ends} | ${item.status}`}
            />
          </List.Item>
        )}
      />
    </>
  );
};
export default Results;
