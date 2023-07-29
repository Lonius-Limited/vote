import React, { useState } from "react";
import { Button, Col, Form, Input, Row } from "antd";
import { useFrappeAuth } from "frappe-react-sdk";
import { _defaultHeaders } from "../api/queries";
import { getCookie, setCookie } from "../lib/cookies";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
const LoginV3 = () => {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({});

  const onFinish = async (values) => {
    const { pf_number } = values;
    setCookie("pf_number", pf_number, 12);
    navigate("/otp-confirm");
  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };
  useEffect(() => {
    const voterValidated = getCookie("voter_validated");
    const userId = getCookie("user_id");
    if (voterValidated) {
      navigate("/ballot");
    }
    if (!voterValidated && userId !== "Guest") {
      navigate("/otp-confirm");
    }
  }, []);
  return (
    <>
      {/* <Row>
        <Col span={6}></Col>
        <Col span={12}>Please enter your PF Number and Click Proceed</Col>
        <Col span={6}></Col>
      </Row> */}
      <Row
        gutter={[16, 16]}
        style={{
          display: "flex",
          alignItems: "center",
          justifyItems: "center",
          justifyContent: "center",
        }}
      >
        <Col>
          <Form
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
            <Form.Item
              label="PF Number"
              name="pf_number"
              rules={[
                {
                  required: true,
                  message:
                    "Please input your institution Personal File Number!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button type="primary" htmlType="submit">
                PROCEED
              </Button>
            </Form.Item>
          </Form>
        </Col>
      </Row>
    </>
  );
};

export default LoginV3;
