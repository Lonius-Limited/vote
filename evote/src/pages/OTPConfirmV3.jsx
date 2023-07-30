import {
  ClockCircleOutlined,
  RollbackOutlined,
  UserOutlined,
} from "@ant-design/icons";
import { Button, Col, Input, Row, Statistic, message, Alert } from "antd";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { _defaultHeaders } from "../api/queries";
import { getCookie, setCookie } from "../lib/cookies";
import {
  useFrappeAuth,
  useFrappeGetCall,
  useFrappePostCall,
  useFrappePutCall,
} from "frappe-react-sdk";
const { Countdown } = Statistic;
// import { Alert } from "antd";
import { authPw, authUid } from "../lib/auth";

const OTPConfirmV3 = () => {
  const navigate = useNavigate();
  const [sendOTPStatus, setSendOTPStatus] = useState(false);//Toggle Start Timer
  const [otpString, setOTPString] = useState("");

  const stageOTPmethod = "vote.utils.election_details.stage_otp";
  const validateOTPMethod = "vote.utils.election_details.authenticate_otp";
  const { currentUser, login } = useFrappeAuth();
  const { call: authentiCateEnteredOTP } = useFrappePutCall(validateOTPMethod);
  const { call: sendOTPToVoter } = useFrappePostCall(stageOTPmethod);
  //handleValidateOTP
  const handleValidateOTP = async (voterRegistrationDetails) => {
    const { voter_id } = voterRegistrationDetails;
    const params = { voter_id, key: otpString };
    // reset();
    await authentiCateEnteredOTP(params)
      .then((result) => {
        if (Object.keys(result).includes("error")) {
          message.error(JSON.stringify(result));
          return;
        }
        setCookie("voter_validated", true, 12);
        if (getCookie('user_id') === "Guest") {
          login(authUid, authPw);
        }
        window.location.href ="/evote/ballot"
        // navigate("/ballot");
      })
      .catch((error) => {
        message.error(error?.message);
      });
  };
  const handleToggleStartTimer = async () => {
    // await sendOTPtoVoter()
    setSendOTPStatus((prevState) => !sendOTPStatus);
  };
  ///===Handle Send OTP Function
  const handleSendOTP = async (voterRegistrationDetails) => {
    const { voter_id } = voterRegistrationDetails;
    const params = { voter_id };
    // reset();
    await sendOTPToVoter(params)
      .then((result) => {
        message.success("OTP sent successfully");
      })
      .catch((error) => {
        message.error(error?.message);
      });
  };

  useEffect(() => {
    const validated = getCookie("voter_validated");
    const userId = getCookie("user_id");
    const pf = getCookie("pf_number");

    if (!validated && userId === "Guest" && !pf) {
      navigate("/login");
    }
    if (validated && userId !== "Guest") {
      // navigate("/ballot");
      window.location.href ="/evote/ballot"
    }
  }, []);
  //End Handle Send OTP

  const pf_number = getCookie("pf_number");
  if (!pf_number) {
    navigate("/login");
  }
  const params = { pf_number };

  const method = "vote.utils.election_details.authenticate_by_pf";
  const { data, error, isValidating, mutate } = useFrappeGetCall(
    method,
    params,
    _defaultHeaders
  );
  if (isValidating) {
    return (
      <Alert
        message="Please wait as we validate your PF Number"
        type="success"
      />
    );
  }
  if (error) {
    return (
      <>
        <Alert message={JSON.stringify(error)} type="error" />
        <Button type="link" onClick={() => navigate("/login")}>
          Back To login
        </Button>
      </>
    );
  }
  if (data) {
    if (Object.keys(data.message).includes("error")) {
      return (
        <>
          <Alert message={JSON.stringify(data)} type="success" />{" "}
          <Button type="link" onClick={() => navigate("/login")}>
            Back To login
          </Button>
        </>
      );
    } else {
      const { cell_number, name, member_id } = data.message;

      const voter_registration_details = { voter_id: name, member_id };
      setCookie(
        "voter_registration_details",
        JSON.stringify(voter_registration_details),
        12
      );
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
                {cell_number || cell_number !== "" ? (
                  <p>Enter the Verification Code sent to {cell_number}</p>
                ) : (
                  <p>
                    Sorry, we do not have a valid phone number in our records
                    please contact institution Management.
                  </p>
                )}
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
                  onClick={() => {
                    handleSendOTP(voter_registration_details);
                    handleToggleStartTimer();
                  }}
                  disabled={sendOTPStatus}
                >
                  Send me an OTP
                </Button>
              </Col>
              <Col sm={24} md={12} lg={12}>
                <Input
                  placeholder="Insert OTP"
                  prefix={<ClockCircleOutlined />}
                  onChange={(e) => setOTPString((prev) => e.target.value)}
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
                <Button
                  type="primary"
                  htmlType="submit"
                  block
                  onClick={() => handleValidateOTP(voter_registration_details)}
                  disabled={parseInt(otpString.length) < 4}
                >
                  VERIFY OTP
                </Button>
              </Col>
            </Row>
            {sendOTPStatus ? (
              <Row>
                {/* <SendOTP /> */}
                <ResetPasswordCountDown
                  handleToggleSendOTP={handleToggleStartTimer}
                />
              </Row>
            ) : null}
          </div>
        </>
      );
    }
  }
};

const ResetPasswordCountDown = ({ handleToggleSendOTP }) => {
  const [deadline, setDeadline] = useState(Date.now() + 1000 * 60); //* 60; //* 24 * 2 + 1000 * 30; // Dayjs is also OK
  const onFinish = () => {
    console.log("finished!");
  };
  return (
    <>
      <Countdown
        title="Time remaining before OTP expires"
        value={deadline}
        onFinish={onFinish}
        onChange={(val) => {
          if (val <= 0) handleToggleSendOTP();
        }}
      />
    </>
  );
};

export default OTPConfirmV3;
