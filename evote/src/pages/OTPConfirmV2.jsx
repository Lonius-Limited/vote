import {
  ClockCircleOutlined,
  RollbackOutlined,
  UserOutlined,
} from "@ant-design/icons";
import { Button, Col, Input, Row, Statistic } from "antd";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { _defaultHeaders } from "../api/queries";
import { getCookie, setCookie } from "../lib/cookies";
import { useFrappeGetCall } from "frappe-react-sdk";
const { Countdown } = Statistic;
const OTPConfirmV2 = () => {
  const [sendOTPStatus, setSendOTPStatus] = useState(false);

  const handleToggleSendOTP = () => {
    setSendOTPStatus((prevState) => !sendOTPStatus);
  };
  const navigate = useNavigate();
  const loginCredentials = getCookie("user_id");
  if (!loginCredentials) {
    navigate("/login");
  }

  const  user_id  = decodeURIComponent(loginCredentials);

  const params = { user_id };

  const method = "vote.utils.election_details.fetch_voter_detail";
  const { data, error, isValidating, mutate } = useFrappeGetCall(
    method,
    params,
    _defaultHeaders
  );
  if (isValidating) {
    return <p>Please wait as we fetch your voter info</p>;
  }
  if (error) {
    return <p>{JSON.stringify(error)}</p>;
  }
  if (data) {
    //fetch_voter_detail
    const {voter_id, member_id} = data;
    setCookie("voter_ids",voter_ids, 2)
    return (
      <>
      
        <div
          style={{
            margin: "0 30% 0 30%",
            borderColor: "1px solid blue",
          }}
        >
          <Row>
            <Col span={6}></Col>
            <Col span={12}>
              <p>Verification Code</p>
            </Col>
            <Col span={6}></Col>
            <hr />
          </Row>
          <Row
            gutter={[16, 16]}
            //   style={{
            //     width: "100%",
            //   }}
          >
            <Col sm={24} md={12} lg={12}>
              <Button
                type="primary"
                htmlType="submit"
                block
                onClick={() => handleToggleSendOTP()}
                disabled={sendOTPStatus}
              >
                Send me an OTP
              </Button>
            </Col>
            <Col sm={24} md={12} lg={12}>
              <Input
                placeholder="Insert OTP"
                prefix={<ClockCircleOutlined />}
              />
            </Col>
          </Row>
          <br />
          <br />
          <Row gutter={[16, 16]}>
            <Col sm={24} md={12} lg={12}>
              <Button
                type="link"
                htmlType="submit"
                block
                danger
                icon={<RollbackOutlined />}
                onClick={() => navigate("/login")}
              >
                CANCEL
              </Button>
            </Col>
            <Col sm={24} md={12} lg={12}>
              <Button type="primary" htmlType="submit" block>
                VERIFY OTP
              </Button>
            </Col>
          </Row>
          {sendOTPStatus ? (
            <Row>
              <ResetPasswordCountDown
                handleToggleSendOTP={handleToggleSendOTP}
              />
            </Row>
          ) : null}
        </div>
      </>
    );
  }
};
const ResendCodeAction = ({ handleResendAction }) => {
  const navigate = useNavigate();
  const loginCredentials = getCookie("user_id");

  if (!loginCredentials) {
    navigate("/login");
  }

  const { voter_id } = JSON.parse(loginCredentials);

  const params = { voter_id };

  const method = "vote.utils.election_details.stage_otp";
  const { data, error, isValidating, mutate } = useFrappeGetCall(
    method,
    params,
    _defaultHeaders
  );
  if (isValidating) {
    return (
      <>
        <p>Resending...</p>
      </>
    );
  }
  if (error) {
    return <>{JSON.stringify(error)}</>;
  }
  if (data) {
    handleResendAction();
    return <p>Sent.</p>;
  }

  return <p>{loginCredentials}</p>;
};
const ResetPasswordCountDown = ({ handleToggleSendOTP }) => {
  const [deadline, setDeadline] = useState(Date.now() + 1000 * 60); //* 60; //* 24 * 2 + 1000 * 30; // Dayjs is also OK
  const onFinish = () => {
    console.log("finished!");
  };
  return (
    <>
      <Countdown
        title="Time remaining before tan expires"
        value={deadline}
        onFinish={onFinish}
        onChange={(val) => {
          if (val <= 0) handleToggleSendOTP();
        }}
      />
    </>
  );
};
export default OTPConfirmV2;
