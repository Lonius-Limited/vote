import React from "react";
import { Descriptions, Row, Statistic } from "antd";

const ElectionSummary = ({ data }) => {
  const {status} = data;
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
          <b style={{color:"blue"}}>{data.status}</b>
          {/* <Statistic
            title="Status"
            value={data.status}
            style={{
              marginRight: 32,
            }}
          /> */}
        </Descriptions.Item>
      </Descriptions>
    </>
  );
};
export default ElectionSummary;
