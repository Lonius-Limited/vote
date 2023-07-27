import React, { useEffect, useState } from "react";
import { Button, Checkbox, Form, Input, Statistic } from "antd";
import { useNavigate } from "react-router-dom";
import { getCookie } from "../lib/cookies";
import { useFrappeGetCall } from "frappe-react-sdk";
import { _defaultHeaders } from "../api/queries";
import { UnlockOutlined } from "@ant-design/icons";

const { Countdown } = Statistic;

const OTPConfirm = () => {
  const [resendOTP, setResendOTP] = useState(false);
  const onFinish = (values) => {
    console.log("Success:", values);
  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };
  const navigate = useNavigate();

  useEffect(() => {
    const loginCredentials = getCookie("voter_login_credentials");

    if (!loginCredentials) {
      navigate("/login");
      // return
    }
  }, []);

  // if (getCookie("voter_login_credentials");)
  return (
    <>
      <div>
        <Form
          title="Verify OTP Code"
          name="basic"
          labelCol={{
            span: 8,
          }}
          wrapperCol={{
            span: 16,
          }}
          style={{
            maxWidth: 1000,
          }}
          initialValues={{
            remember: true,
          }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          autoComplete="off"
        >
          <Form.Item>
            <h3 style={{ color: "blue" }}>Verify OTP</h3>
          </Form.Item>
          <Form.Item
            label="OTP Code"
            name="otp_code"
            rules={[
              {
                required: true,
                message: "Please input the OTP Code you received on SMS!",
              },
            ]}
          >
            <Input
              size="default size"
              placeholder="Type the OTP Code here"
              prefix={<UnlockOutlined />}
            />
          </Form.Item>
          <Form.Item
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            <Button type="primary" htmlType="submit">
              VERIFY
            </Button>
            <Button type="secondary" onClick={() => navigate("/login")}>
              BACK
            </Button>
          </Form.Item>
          <Form.Item>
            <ResetPasswordCountDown />
          </Form.Item>
        </Form>
      </div>
    </>
  );
};
const VerifyOTP = ({ otpCode }) => {
  return (
    <>
      <p>verifying</p>
    </>
  );
};
const ResendCodeAction = ({ handleResendAction }) => {
  const navigate = useNavigate();
  const loginCredentials = getCookie("voter_login_credentials");

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

const ResetPasswordCountDown = () => {
  const [deadline, setDeadline] = useState(Date.now() + 1000 * 60); //* 60; //* 24 * 2 + 1000 * 30; // Dayjs is also OK
  const [btnBisabled, setBtnBisabled] = useState(true);
  const [resendOTP, setResendOTP] = useState(false);
  const handleResendAction = () => {
    setResendOTP((prevState) => !resendOTP);
  };
  const onFinish = () => {
    console.log("finished!");
  };
  return (
    <>
      <Button
        disabled={btnBisabled}
        onClick={() => {
          setBtnBisabled((prevState) => !btnBisabled);
          setDeadline((prevState) => Date.now() + 1000 * 60);
          handleResendAction();
        }}
      >
        Resend OTP
      </Button>
      <Countdown
        title=""
        value={deadline}
        onFinish={onFinish}
        onChange={(val) => {
          if (val <= 0) setBtnBisabled((prevState) => !btnBisabled);
        }}
      />
      {resendOTP ? (
        <ResendCodeAction handleResendAction={handleResendAction} />
      ) : null}
    </>
  );
};
export default OTPConfirm;
