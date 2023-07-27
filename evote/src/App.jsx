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
            path="/results"
            exact
            element={
              <Protected>
                <Ballot>
                  <Results />
                </Ballot>
              </Protected>
            }
          />
        </Routes>
      </Router>
    </>
  );
};

export default App;
