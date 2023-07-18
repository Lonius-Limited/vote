import { Button, Col, Row } from "antd";
import React from "react";
import electionSVG from "../public/undraw_election_day_w842.svg";
import { Carousel } from "antd";
import { useNavigate } from "react-router-dom";
import "./App.css";
const Index = () => {
  const navigate = useNavigate();
  const gotoBallot = () => {
    navigate("/ballot");
  };
  return (
    <>
      <Row>
        <Col
          xs={24}
          sm={24}
          md={24}
          lg={12}
          xl={12}
          
        >
          <h1>Choose your leadership</h1>
          <Carousel123 />
          <Button type="primary" onClick={() => gotoBallot()}>
            Login to Vote
          </Button>
        </Col>
        <Col>
          <img
            className="landingImg"
            src={electionSVG}
            alt="Elections SVG"
          />
        </Col>
      </Row>
    </>
  );
};
const Carousel123 = () => {
  const contentStyle = {
    height: "260px",
    color: "#fff",
    lineHeight: "260px",
    textAlign: "center",
    background: "#8F68EF",
  };
  return (
    <Carousel autoplay>
      <div>
        <h3 style={contentStyle}>Login with your VoterID and OTP</h3>
      </div>
      <div>
        <h3 style={contentStyle}>Select Your candidate for each position</h3>
      </div>
      <div>
        <h3 style={contentStyle}>Submit your ballot</h3>
      </div>
    </Carousel>
  );
};

export default Index;
