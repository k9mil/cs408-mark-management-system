import * as React from "react";

import Sidebar from "../../common/Sidebar";

const MarksPage = () => {
  return (
    <div className="bg-primary-blue h-screen w-screen flex justify-row">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl"></div>
    </div>
  );
};

export default MarksPage;
