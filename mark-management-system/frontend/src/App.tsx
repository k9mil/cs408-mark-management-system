// import './index.css'
import React from "react";
import Routes from "./Routes";
import { Toaster } from "sonner";

function App() {
  return (
    <>
      <Toaster richColors />
      <Routes />
    </>
  );
}

export default App;
