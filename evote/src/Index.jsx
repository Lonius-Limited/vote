import { Button, Col, Row, Card } from "antd";
import React from "react";
import electionSVG from "../public/undraw_election_day_w842.svg";
import { Carousel } from "antd";
import { useNavigate } from "react-router-dom";
import "./App.css";
const Index = () => {
  const navigate = useNavigate();
  const gotoBallot = () => {
    navigate("/login");
  };
  return (
    <>
      <Row>
        <Col sm={24} md={24} lg={12}>
          <h1>Choose your leadership</h1>
          <Carousel123 />
          <Button type="primary" onClick={() => gotoBallot()}>
            Login to Vote
          </Button>
        </Col>
        <Col>
          <img className="landingImg" src={electionSVG} alt="Elections SVG" />
        </Col>
      </Row>
    </>
  );
};
const Carousel123 = () => {
  const contentStyle = {
    // height: "260px",
    color: "#fff",
    // lineHeight: "260px",
    textAlign: "center",
    background: "#8F68EF",
    padding: "54px"
  };
  return (
    <Carousel autoplay motionDurationSlow ='5s'>
      <div>
        {/* <h3 style={contentStyle}>Login with your PF Number and OTP - In order to vote, you are required to securely login to the platform. Please use your employer Personal File (PF). We will send you a One Time Password (OTP) to your phone number in our records.</h3> */}
        <Card title="Login with your PF Number and OTP" bordered={false} style={contentStyle}>
          <p>In order to vote, you are required to securely login to the platform. Please use your employer Personal File (PF). We will send you a One Time Password (OTP) to your phone number in our records.</p>
          <p></p>
          <p></p>
        </Card>
      </div>
      <div>
        <Card title="Select Your candidate for each position" bordered={false} style={contentStyle}>
          <p>After you have securely logged in, you will be able to proceed to the voting page. In this page, you will be provided with a list of candidates for each position. You are expected to pick your choice from among the available candidates. The choices you pick are to a maximum available for the position.</p>
          <p></p>
          <p></p>
        </Card>
      </div>
      <div>
        <h3 style={contentStyle}>Submit your ballot</h3>
      </div>
    </Carousel>
  );
};

export default Index;
