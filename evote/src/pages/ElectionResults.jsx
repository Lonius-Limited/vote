import React from "react";
import { useParams } from "react-router-dom";
// import { ArrowDownOutlined, ArrowUpOutlined } from "@ant-design/icons";
import {
  Card,
  Col,
  Result,
  Row,
  Statistic,
  Descriptions,
  Avatar,
  List,
  Progress,
  Empty,
} from "antd";
import { useFrappeGetCall } from "frappe-react-sdk";
import { _defaultHeaders } from "../api/queries";
import { getCookie } from "../lib/cookies";

const ElectionResults = () => {
  const { election } = useParams();

  const { voter_id } = JSON.parse(getCookie("voter_registration_details"));

  const params = { election, voter: voter_id };
  const swrOptions ={refreshInterval: 60000}
  const method = "vote.utils.election_details.get_election_results_v3";
  const { data, error, isValidating } = useFrappeGetCall(
    method,
    params,
    _defaultHeaders,
    swrOptions
  );
  if (isValidating) {
    return <>Loading...</>;
  }
  if (error) {
    return <>{JSON.stringify(error)}</>;
  }

  if (data) {
    const { all_results, institution } = data.message;
    /*
    [
    {
        "id": 1,
        "branch": "MTRHSPS STATION",
        "position": "MTRH Pension Trustee",
        "eligible_voters": 3671,
        "turnout": 3,
        "turnout_percent": 0.08172160174339417,
        "tally": [
            {
                "candidate_id": "V0010744",
                "candidate": "SOLOMON, KIPYEGO TANUI",
                "votes": 2,
                "headshot": "http://demo.elections.co.ke/files/tanui.jpeg"
            },
            {
                "candidate_id": "V0011809",
                "candidate": "FELIX, KOECH",
                "votes": 1,
                "headshot": "http://demo.elections.co.ke/files/felix_koech.jpg"
            }
        ]
    }
]
    */
    const allStats = all_results;
    if (allStats.length < 1) {
      return (
        <>
          <Result
            status="warning"
            title="Sorry, no elections statistics for now."
            extra={
              <Button
                type="primary"
                key="console"
                onClick={() => (window.location.href = "/evote/logout")}
              >
                Log Me Out
              </Button>
            }
          />
        </>
      );
    }

    // return <p>{JSON.stringify(allStats)}</p>
    return (
      <>
        {allStats.map((selectedPosition) => {
          const {
            position,
            branch,
            tally,
            eligible_voters,
            turnout,
            turnout_percent,
          } = selectedPosition;
          const totalVotesCast = tally
            .map((r) => parseInt(r.votes))
            .reduce((a, b) => a + b, 0);

          const notVoted = eligible_voters - turnout;
          const summaryPayload = {
            eligible_voters,
            turnout,
            turnout_percent,
            notVoted,
          };
          return (
            <>
              <div
                style={{
                  width: "90%",
                  minWidth: "90%",
                }}
              >
                <Descriptions title="Position Stats">
                  <Descriptions.Item label="Position">
                    {`${branch} / ${position}`}
                  </Descriptions.Item>
                </Descriptions>

                <ElectionStats payload={summaryPayload} />
                <CandidatesSummary candidateResults={tally} turnout={turnout} />
              </div>
            </>
          );
        })}
      </>
    );
  }
};
const ElectionStats = ({ payload }) => {
  const { eligible_voters, turnout, turnout_percent, notVoted } = payload;

  return (
    <>
      <Descriptions title="Candidate Results"></Descriptions>
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card bordered={false}>
            <Statistic
              title="Eligible Voters"
              value={eligible_voters}
              // precision={2}
              valueStyle={{
                color: "#3f8600",
                fontSize: "48",
              }}
              // prefix={<ArrowUpOutlined />}
              suffix=""
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card bordered={false}>
            <Statistic
              title="Voted"
              value={turnout}
              // precision={2}
              valueStyle={{
                color: "#3f8600",
              }}
              // prefix={<ArrowDownOutlined />}
              suffix=""
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card bordered={false}>
            <Statistic
              title="Not Voted"
              value={notVoted}
              // precision={0}
              valueStyle={{
                color: "#3f8600",
              }}
              // prefix={<ArrowUpOutlined />}
              suffix=""
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card bordered={false}>
            <Statistic
              title="Turnout (%)"
              value={turnout_percent}
              precision={2}
              valueStyle={{
                color: "#3f8600",
              }}
              // prefix={<ArrowDownOutlined />}
              suffix="%"
            />
          </Card>
        </Col>
      </Row>
    </>
  );
};
const CandidatesSummary = ({ candidateResults, turnout }) => {
  // /[
  //   {
  //       "candidate_id": "V0010744",
  //       "candidate": "SOLOMON, KIPYEGO TANUI",
  //       "votes": 2,
  //       "headshot": "http://demo.elections.co.ke/files/tanui.jpeg"
  //   },
  //   {
  //       "candidate_id": "V0011809",
  //       "candidate": "FELIX, KOECH",
  //       "votes": 1,
  //       "headshot": "http://demo.elections.co.ke/files/felix_koech.jpg"
  //   }
  // ]
  if (candidateResults.length < 1) {
    return <Empty description={false} />;
  }
  const sortByVotes = (a, b) => {
    if (a.votes < b.votes) {
      return -1;
    }
    if (a.votes > b.votes) {
      return 1;
    }
    return 0;
  };
  return (
    <List
      itemLayout="horizontal"
      dataSource={candidateResults.filter(b=>!b.absconded).sort(sortByVotes).reverse()}
      renderItem={(item, index) => (
        <List.Item>
          <List.Item.Meta
            avatar={
              <Avatar size={80} src={item.headshot} alt={item.candidate} />
            }
            title={`${item.candidate}-(${item.votes} votes.)`}
            description={
              <Progress
                percent={(100 * parseFloat(item.votes)) / parseFloat(turnout)}
                status="active"
                format={(percent) => percent.toFixed(2) + "%"}
              />
            }
          />
        </List.Item>
      )}
    />
  );
};
export default ElectionResults;
