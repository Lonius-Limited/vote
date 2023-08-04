import {
  Breadcrumb,
  Layout,
  Menu,
  theme,
  Row,
  Col,
  Button,
  Image,
  Avatar,
} from "antd";
import { PoweroffOutlined, CheckSquareOutlined } from "@ant-design/icons";
import "./App.css";
import evoteImage from "../public/eVote Logo.png";
// import { useNavigate } from "react-router-dom";
const { Header, Content, Footer } = Layout;

const MainLayoutV2 = ({ children }) => {
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  // const navigate = useNavigate()
  return (
    <>
      <Layout>
        <Header
          style={{
            position: "sticky",
            top: 0,
            zIndex: 1,
            width: "100%",
            minWidth: "100%",
            // display: "flex",
            // alignItems: "center",
            background: colorBgContainer,
          }}
        >
          <Row style={{ width: "100%", minWidth: "100%" }}>
            <Col span={1}></Col>
            <Col span={4}>
              <Avatar
                src={evoteImage}
                size={{
                  xs: 80,
                  sm: 80,
                  md: 80,
                  lg: 100,
                  xl: 100,
                  xxl: 100,
                }}
                alt="MTRHSPS Logo"
                // onClick={()=>navigate("/")}
              />
            </Col>
            {/* <Col span={4}><h2>MTRHSPS eVote</h2></Col> */}
            <Col span={17}></Col>
            <Col span={1}>
              <Button
                type="primary"
                icon={<PoweroffOutlined />}
                onClick={() => window.location.href="/evote/logout"}
              ></Button>
            </Col>
            <Col span={1}></Col>
          </Row>
        </Header>
        <Content
          className="site-layout"
          style={
            {
              // padding: "0 10px",
            }
          }
        >
          <br />
          <br />
          <br />
          <div
            style={{
              // padding: 24,
              // margin: 24,
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
export default MainLayoutV2;
