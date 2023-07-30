import React from "react";
import { Descriptions, Row, Statistic } from "antd";

const ElectionSummary = ({ data }) => {
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
export default ElectionSummary;
