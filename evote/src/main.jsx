import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import { Authorization, apiHost } from "./lib/auth";
import { FrappeProvider } from "frappe-react-sdk";
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    {/* <FrappeProvider url={apiHost}> */}
    <FrappeProvider url="">
      <App />
    </FrappeProvider>
  </React.StrictMode>
);
