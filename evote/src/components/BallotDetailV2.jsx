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
  Modal,
  Popconfirm,
  notification
} from "antd";
import { useState } from "react";
import { useFrappePostCall } from "frappe-react-sdk";
import { Navigate, useNavigate } from "react-router-dom";
import { getCookie } from "../lib/cookies";
const BallotDetailV2 = ({ data }) => {
  const [api, contextHolder] = notification.useNotification();

  const navigate = useNavigate();
  const { ballot_data, election } = data;

  //Modal
  const [open, setOpen] = useState(false);
  const showModal = () => {
    setOpen(!open);
  };
  //Election and Voter

  //End Election and voter
  //EndModal
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
      parseInt(candidates.filter((r) => parseInt(r.choice) === 1).length) >=
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
      return;
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
  // post_e_ballot(voter, election, ballot_data)
  const postVoterBallotMethod = "vote.utils.election_details.post_e_ballot";
  const { call: postVoterBallot } = useFrappePostCall(postVoterBallotMethod);
  const handleSubmitBallot = async () => {
    const { name } = JSON.parse(getCookie("active_elections"));
    const { voter_id } = JSON.parse(getCookie("voter_registration_details"));
    const params = {
      voter: voter_id,
      election: name,
      ballot_data: JSON.stringify(ballotData),
    };

    await postVoterBallot(params)
      .then((result) => {
        if (Object.keys(result).includes("error")) {
          message.error(JSON.stringify(result));
          return;
        }
        navigate("/ballot-submit", {
          state: {
            ballotResult: result,
          },
        });
        // navigate("/ballot");
      })
      .catch((error) => {
        message.error(error?.message);
      });
  };
  const openNotification = (message, description) => {
    api.open({
      message: {message},
      description:
        {description},
      duration: 0,
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
        <VoteSummary data={data} />
        <Popconfirm
          style={{ right: 0 }}
          title="Cast Ballot"
          description="Are you sure to Cast your Ballot? Please check your ballot selections before clicking Yes."
          okText="Yes"
          cancelText="No"
          onConfirm={() => {
            const abscondedBallots = ballotData
              .map((position) => {
                const { candidates, maximum_number_of_positions } = position;
                const choices = candidates.filter(
                  (x) => parseInt(x.choice) === 1
                );
                const absconded =
                  choices.length != parseInt(maximum_number_of_positions);

                return { absconded, position: position.position };
              })
              .filter((x) => x.absconded);

            if (abscondedBallots.length > 0) {
              message.error(
                `Sorry, you have not selected the maximum number candidates you can vote for under the following positions ${abscondedBallots.map(
                  (x) => x.position
                )}`
              );
              return;
            }

            handleSubmitBallot();
          }}
          onCancel={() => message.success("Action cancelled.")}
        >
          <Button primary>Submit Ballot Data</Button>
        </Popconfirm>
        {/* {JSON.stringify({ ballotData })} */}
        {ballotData.map((positionData, idx) => {
          const { candidates, position } = positionData;
          return (
            <>
              <Card
                title={`${idx + 1}.${position}`}
                extra={
                  <>
                    <Statistic
                      title="Maximum Allowed Positions:"
                      value={positionData.maximum_number_of_positions}
                    />
                  </>
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
                      onClick={() =>
                        handleAddToBallotChoice({
                          candidateId: item.candidate_id,
                          positionSelected: position,
                        })
                      }
                      style={{
                        backgroundColor:
                          parseInt(item.choice) === 1 ? "#d3ebd7" : null,
                      }}
                      actions={[
                        <Checkbox
                          checked={parseInt(item.choice)}
                          disabled={true}
                          onChange={(checkedValue) =>
                            console.log(checkedValue.target.checked)
                          }
                        ></Checkbox>,
                        // <Button
                        //   type={parseInt(item.choice) ? "danger" : "primary"}
                        //   size="large"
                        //   onClick={() =>
                        //     handleAddToBallotChoice({
                        //       candidateId: item.candidate_id,
                        //       positionSelected: position,
                        //     })
                        //   }
                        // >
                        //   {parseInt(item.choice) ? "UNVOTE" : "VOTE"}
                        // </Button>,
                        // <DeleteRowOutlined />,
                      ]}
                    >
                      <List.Item.Meta
                        avatar={
                          <Avatar
                            size={100}
                            shape="circle"
                            src={item.headshot}
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
      {/* ballotData, openStatus, toggleOpenStatus */}
      {open ? (
        <ConfirmBallotChoice
          ballotData={ballotData}
          openStatus={open}
          toggleOpenStatus={showModal}
        />
      ) : null}
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
const ConfirmBallotChoice = ({ ballotData, openStatus, toggleOpenStatus }) => {
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [modalText, setModalText] = useState("Following are your selections:");

  const handleOk = () => {
    setModalText("Posting your ballot");
    setConfirmLoading(true);
    // setTimeout(() => {
    //   setOpen(false);
    //   setConfirmLoading(false);
    // }, 2000);
    toggleOpenStatus();
    setConfirmLoading(false);
  };
  const handleCancel = () => {
    console.log("Clicked cancel button");
    toggleOpenStatus();
  };
  return (
    <>
      {/* <Button type="primary" onClick={showModal}>
        Open Modal with async logic
      </Button> */}
      <Modal
        title="Confirmation"
        open={open}
        onOk={handleOk}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
      >
        <>
          <p>{modalText}</p>
          {JSON.stringify(ballotData)}
        </>
      </Modal>
    </>
  );
};
export default BallotDetailV2;
