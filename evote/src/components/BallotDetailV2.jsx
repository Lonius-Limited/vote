import React from "react";
import { Card, Avatar, List, Statistic, Checkbox, Button, message } from "antd";
import { useContext } from "react";
import BallotContext from "../BallotContext";
import { useState } from "react";
const BallotDetailV2 = ({ data }) => {
  const { ballot_data } = data;
  const [ballotData, setBallotData] = useState(ballot_data);
  const handleAddToBallotReceipt = (candidateSelection) => {
    //
    const { candidateId, positionSelected } = candidateSelection;
    // message.success(`${JSON.stringify(candidateSelection)}`);
    setBallotData((prevState) => {
      let ballotCopy = [...prevState];
      const value = parseInt(
        ballotCopy
          .filter((p) => p.position === positionSelected)[0]
          .candidates.find((c) => c.candidate_id === candidateId).choice
      );
      const newChoice = value === 1 ? 0 : 1;
      return (ballotCopy
        .filter((p) => p.position === positionSelected)[0]
        .candidates.find((c) => c.candidate_id === candidateId).choice =
        newChoice);
    });
  };
  return (
    <>
      <div
        style={{
          width: "90%",
          minWidth: "90%",
        }}
      >
        {JSON.stringify(ballotData)}
        {ballotData.map((positionData, idx) => {
          const { candidates, position } = positionData;
          return (
            <>
              <Card
                title={`Using State: ${idx + 1}.${position}`}
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
                            handleAddToBallotReceipt({
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

export default BallotDetailV2;
