import {
  Avatar,
  List,
  Checkbox,
  message,
  Descriptions,
  Button,
  Col,
  Row,
} from "antd";
import React from "react";
import { useContext } from "react";
import BallotContext from "../BallotContext";

const BallotDetail = ({ data }) => {
  const { ballotReceipt, addToBallotReceipt } = useContext(BallotContext);
  const handlePostBallot = () => {};
  const { ballot_data } = data;

  return (
    <>
      {ballot_data.map((positionData) => {
        return (
          <>
            <Row>
              <Col span={24}>
                <Descriptions title={positionData.position}>
                  <Descriptions.Item label="Branch">
                    {positionData.branch}
                  </Descriptions.Item>
                  <Descriptions.Item label="Maximum Selectable Candidates">
                    {positionData.maximum_number_of_positions}
                  </Descriptions.Item>
                </Descriptions>
              </Col>
            </Row>
            <PositionData positionData={positionData}/>
          </>
        );
      })}
    </>
  );
};
const PositionData = ({ positionData }) => {
  return (
    <>
      <Row>
        <Col span={24}>
          {positionData.candidates.map((candidate) => {
            const { position, branch, maximum_number_of_positions } =
              positionData;
            const positionDetails = {
              position,
              branch,
              maximum_number_of_positions,
            };
            return (
              <>
                <PositionCandidate
                  candidateProfile={candidate}
                  positionProfile={positionDetails}
                />
              </>
            );
          })}
        </Col>
      </Row>
    </>
  );
};
const PositionCandidate = ({ candidateProfile, positionProfile }) => {
  //(object, string)
  //Business Logic
  const data = [candidateProfile];
  const { ballotReceipt, addToBallotReceipt } = useContext(BallotContext);
  const handlePostBallot = () => {};
  return (
    <>
      <List
        itemLayout="horizontal"
        dataSource={data}
        renderItem={(item, index) => (
          <List.Item>
            <List.Item.Meta
              avatar={
                <Avatar
                  src={`https://xsgames.co/randomusers/avatar.php?g=pixel&key=${index}`}
                />
              }
              title={<a href="https://ant.design"></a>}
              description="Ant Design, a design language for background applications, is refined by Ant UED Team"
            />
          </List.Item>
        )}
      />
      {/* <List
        itemLayout="horizontal"
        dataSource={data}
        renderItem={(item, index) => (
          <List.Item>
            <List.Item.Meta
              avatar={
                <Avatar
                  src={`https://xsgames.co/randomusers/avatar.php?g=pixel&key=${index}`} //candidateProfile.headshot
                />
              }
              title={item.candidate_name}
              description={item.candidate_id}
            />
            <Checkbox
              checked={parseInt(item.choice)}
              disabled={true}
              onChange={(e) => console.log(e, item)}
            ></Checkbox>
            <Button type="primary" size="small" onClick={() => message.success(`You selected ${item.candidate_name}`)}>
              Vote
            </Button>
          </List.Item>
        )}
      /> */}
    </>
  );
};
export default BallotDetail;
