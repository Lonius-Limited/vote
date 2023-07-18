import { Breadcrumb, Layout, Menu, theme } from "antd";
const { Header, Content, Footer } = Layout;
const MainLayout = ({ children }) => {
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  return (
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
        <div className="demo-logo" />
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
  );
};
export default MainLayout;
