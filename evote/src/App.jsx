import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Index from "./Index";
import MainLayout from "./MainLayout";
import Ballot from "./pages/Ballot";
import Results from "./pages/Results";
import Protected from "./Protected";

import LoginV3 from "./pages/LoginV3";
import OTPConfirmV3 from "./pages/OTPConfirmV3";
import { BallotProvider } from "./BallotContext";
import Logout from "./components/Logout";
import BallotSubmit from "./pages/BallotSubmit";
import VotingPage from "./pages/VotingPage";
function App() {
  return (
    <div className="App">
      <MainLayout>
        <AppRoutes />
      </MainLayout>
    </div>
  );
}

const AppRoutes = () => {
  //Ballot,Login, Results
  return (
    <>
      <Router basename="/evote">
        <Routes>
          <Route path="/" exact element={<Index />} />
          <Route path="/confirm-registration" exact element={<Index />} />
          <Route path="/login" exact element={<LoginV3 />} />
          <Route path="/otp-confirm" exact element={<OTPConfirmV3 />} />
          <Route
            path="/logout"
            exact
            element={
              // <Protected>
              <Logout />
              // </Protected>
            }
          />
          <Route
            path="/ballot"
            exact
            element={
              <Protected>
                <BallotProvider>
                  <Ballot />
                </BallotProvider>
              </Protected>
            }
          />
          <Route
            path="/ballot/:election"
            exact
            element={
              <Protected>
                <BallotProvider>
                  <VotingPage />
                </BallotProvider>
              </Protected>
            }
          />
          <Route
            path="/ballot-submit"
            exact
            element={
              <Protected>
                <BallotProvider>
                  <BallotSubmit />
                </BallotProvider>
              </Protected>
            }
          />
          <Route
            path="/results"
            exact
            element={
              <Protected>
                <Results />
              </Protected>
            }
          />
        </Routes>
      </Router>
    </>
  );
};

export default App;
