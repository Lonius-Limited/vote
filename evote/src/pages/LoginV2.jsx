import React, { useState } from "react";
import { Button, Col, Form, Input, Row } from "antd";
import { useFrappeAuth } from "frappe-react-sdk";
import { _defaultHeaders } from "../api/queries";
import { setCookie } from "../lib/cookies";
import { useNavigate } from "react-router-dom";
const LoginV2 = () => {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({});
  const {
    currentUser,
    isValidating,
    isLoading,
    login,
    logout,
    error,
    updateCurrentUser,
    getUserCookie,
  } = useFrappeAuth();

  const onFinish = async (values) => {
    login(values.login_id, values.password)
      .then((result) => {
        setCookie("voter_login_credentials", JSON.stringify(values.login_id), 12);
        navigate("/otp-confirm");
      })
      .catch((error) => {
        console.log(error)
      });
  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };
  return (
    <>
      <Row
        style={{
          display: "flex",
          alignItems: "center",
          justifyItems: "center",
          justifyContent: "center",
        }}
      >
        <Col
          xs={24}
          sm={24}
          md={24}
          lg={24}
          xl={24}
          xxl={24}
          style={{
            marginRight: "30%",
            marginLeft: "30%",
          }}
        >
          Login v2
        </Col>
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
              label="Login ID (Email or ID)"
              name="login_id"
              rules={[
                {
                  required: true,
                  message: "Please input your Login ID!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              label="Password"
              name="password"
              rules={[
                {
                  required: true,
                  message: "Please input your password",
                },
              ]}
            >
              <Input.Password />
            </Form.Item>

            <Form.Item
              wrapperCol={{
                offset: 8,
                span: 16,
              }}
            >
              <Button type="primary" htmlType="submit">
                LOGIN
              </Button>
            </Form.Item>
          </Form>
        </Col>
      </Row>
    </>
  );
};

export default LoginV2;
