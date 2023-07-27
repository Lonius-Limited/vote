import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import { FrappeProvider } from "frappe-react-sdk";
import { apiHost } from "./lib/auth.js";
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <FrappeProvider url={apiHost}>
      <App />
    </FrappeProvider>
  </React.StrictMode>
);
