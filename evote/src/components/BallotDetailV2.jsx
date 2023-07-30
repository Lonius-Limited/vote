import React from "react";
import {
  Card,
  Avatar,
  List,
  Statistic,
  Checkbox,
  Button,
  message,
  Descriptions,
} from "antd";
import { useState } from "react";
import { useFrappePostCall } from "frappe-react-sdk";
const BallotDetailV2 = ({ data }) => {
  const { ballot_data } = data;
  const [ballotData, setBallotData] = useState(ballot_data);
  // const [ballotChoice, setBallotChoice] = useState(ballot_data);
  const maximumCandidateChoiceAttained = (positionSelected, candidateId) => {
    const positionProfile = ballotData.find(
      (r) => r.position === positionSelected
    ); //I need the object
    const { candidates, maximum_number_of_positions } = positionProfile;

    const { choice } = candidates.find((r) => r.candidate_id === candidateId);

    const newChoice = parseInt(choice) === 1 ? 0 : 1;

    return (
      newChoice === 1 &&
      parseInt(candidates.filter((r) => parseInt(r.choice) === 1).length) >
        parseInt(maximum_number_of_positions)
    );
  };
  const handleAddToBallotChoice = (candidateSelection) => {
    const { candidateId, positionSelected } = candidateSelection;
    //message.success(`${JSON.stringify(candidateSelection)}`);
    // {"candidateId":"MTRHSPS/MTRHSPS/V0012256","positionSelected":"MTRH Pension Trustee"}
    if (maximumCandidateChoiceAttained(positionSelected, candidateId)) {
      message.error(
        `Sorry, you have reached the maximum positions you can vote for under ${positionSelected}`
      );
      return
    }
    setBallotData((prevState) => {
      const ballotCopy = [...prevState];
      const value = parseInt(
        ballotCopy
          .filter((p) => p.position === positionSelected)[0]
          .candidates.find((c) => c.candidate_id === candidateId).choice
      );
      //positionIndex
      const positionIndex = ballotCopy
        .map((r) => r.position)
        .indexOf(positionSelected);
      //candidateIndex
      const positionCandidates = ballotCopy.filter(
        (p) => p.position === positionSelected
      )[0].candidates;
      const candidateIndex = positionCandidates
        .map((r) => r.candidate_id)
        .indexOf(candidateId);
      const newChoice = value === 1 ? 0 : 1;

      ballotCopy[positionIndex].candidates[candidateIndex].choice = newChoice;
      return ballotCopy;
    });
  };

  const handlePostBallot = () => {};
  return (
    <>
      <div
        style={{
          width: "90%",
          minWidth: "90%",
        }}
      >
        <VoteSummary data={data} />
        {/* {JSON.stringify({ ballotData })} */}
        {ballotData.map((positionData, idx) => {
          const { candidates, position } = positionData;
          return (
            <>
              <Card
                title={`${idx + 1}.${position}`}
                extra={
                  <Statistic
                    title="Maximum Allowed Positions:"
                    value={positionData.maximum_number_of_positions}
                  />
                }
                style={{
                  width: "90%",
                  minWidth: "90%",
                }}
              >
                <List
                  itemLayout="horizontal"
                  dataSource={candidates}
                  renderItem={(item, index) => (
                    <List.Item
                      actions={[
                        <Checkbox
                          checked={parseInt(item.choice)}
                          disabled={true}
                          onChange={(checkedValue) =>
                            console.log(checkedValue.target.checked)
                          }
                        ></Checkbox>,
                        <Button
                          type={parseInt(item.choice) ? "danger" : "primary"}
                          size="large"
                          onClick={() =>
                            handleAddToBallotChoice({
                              candidateId: item.candidate_id,
                              positionSelected: position,
                            })
                          }
                        >
                          {parseInt(item.choice) ? "UNVOTE" : "VOTE"}
                        </Button>,
                        // <DeleteRowOutlined />,
                      ]}
                    >
                      <List.Item.Meta
                        avatar={
                          <Avatar
                            size="md"
                            shape="square"
                            src={`https://xsgames.co/randomusers/avatar.php?g=pixel&key=${index}`}
                          />
                        }
                        title={item.candidate_name}
                        description={`#${item.candidate_id}`}
                      />
                    </List.Item>
                  )}
                />
              </Card>
            </>
          );
        })}
      </div>
    </>
  );
};

const VoteSummary = ({ data }) => {
  const { status } = data;
  const statusColorMap = {
    Scheduled: "orange",
    Open: "green",
    Closed: "red",
  };
  return (
    <>
      <Descriptions title="Voter Card">
        <Descriptions.Item label="Election">{data.election}</Descriptions.Item>
        <Descriptions.Item label="Voter Card ID">
          {data.member_id}
        </Descriptions.Item>
        <Descriptions.Item label="Election Start">
          {data.election_start}
        </Descriptions.Item>
        <Descriptions.Item label="Election End">
          {data.election_ends}
        </Descriptions.Item>
        <Descriptions.Item label="Status">
          <b style={{ color: statusColorMap[status] }}>{status}</b>
        </Descriptions.Item>
      </Descriptions>
    </>
  );
};

export default BallotDetailV2;
