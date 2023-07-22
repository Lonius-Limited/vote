import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Index from "./Index";
import MainLayout from "./MainLayout";
import Ballot from "./pages/Ballot";
import Results from "./pages/Results";
import Protected from "./Protected";
import Login from "./pages/Login";

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
          <Route path="/login" exact element={<Login />} />
          <Route
            path="/ballot"
            exact
            element={
              <Protected>
                <Ballot />
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
