import { Breadcrumb, Layout, Menu, theme, Row, Col, Button } from "antd";
import { PoweroffOutlined } from "@ant-design/icons";

const { Header, Content, Footer } = Layout;

const MainLayout = ({ children }) => {
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  return (
    <>
      <Layout>
        <Header
          style={{
            position: "sticky",
            top: 0,
            zIndex: 1,
            width: "100%",
            display: "flex",
            alignItems: "center",
            background: colorBgContainer,
          }}
        >
          <Row style={{ width: "100%", display: "flex" }}>
            <Col span={4} style={{ float: "left" }}>
              eVote
            </Col>
            {/* <Col span={2}></Col>
            <Col span={16}></Col> */}
            <Col
              span={2}
              style={{
                float: "right",
                display: "flex",
                justifyItems: "right",
                alignItems: "right",
              }}
            >
              <Button
                type="primary"
                icon={<PoweroffOutlined />}
                onClick={() => (window.location.href = "/evote/logout")}
              ></Button>
            </Col>
          </Row>
        </Header>
        <Content
          className="site-layout"
          style={{
            padding: "0 20px",
          }}
        >
          <br />
          <br />
          <br />
          <div
            style={{
              padding: 24,
              margin: 24,
              minHeight: 380,
              background: colorBgContainer,
              width: "auto",
              height: "auto",
              maxWwidth: "100%",
              maxHeight: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {children}
          </div>
        </Content>
        <Footer
          style={{
            textAlign: "center",
          }}
        >
          eVote App ©2023
        </Footer>
      </Layout>
    </>
  );
};
export default MainLayout;
