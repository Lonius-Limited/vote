import React from "react";
import { Card, Col, List, Row } from "antd";
// import { useMediaQuery } from "@uidotdev/usehooks";
import useMediaQuery from "use-media-antd-query";

const data = [
  {
    title: "Vote Started: 09:00",
  },
  {
    title: "Votes Cast: 34",
  },
  {
    title: "Total Number of Voters: 1045",
  },
  {
    title: "Turnout(%): 3.25%",
  },
];
/*
{voting_start, vote_ends, votes_cast, total_voter_count }
*/
const ElectionSummary = () => {
  // const isSmallDevice = useMediaQuery("only screen and (max-width : 800px)");

  const colSize = useMediaQuery();
  console.log(colSize); // "xs" | "sm" | "md" | "lg" | "xl" | "xxl"
  return (
    <>
      {["md", "lg", "xl","xxl"].includes(colSize) ? (
        <MultiCardLayout payload={data} />
      ) : (
        <SingleCardlayout payload={data} />
      )}
    </>
  );
};
const MultiCardLayout = ({ payload }) => {
  return (
    <List
      grid={{
        gutter: 16,
        column: 4,
      }}
      dataSource={payload}
      renderItem={(item) => (
        <List.Item>
          <Card title={item.title}>Card content</Card>
        </List.Item>
      )}
    />
  );
};
const SingleCardlayout = ({ payload }) => {
  return (
    <Card title="Election Summary">
      {payload.map((item, index) => (
        <p key={index}>{item.title}</p>
      ))}
    </Card>
  );
};
export default ElectionSummary;
