import React, { useEffect } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/common/Card";

import Sidebar from "../../common/Sidebar";

const DashboardPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center">
        <Card className="w-1/2 h-3/5 space-y-4 p-4 flex flex-col">
          <div className="flex flex-row space-x-8 h-full">
            <Card className="w-1/2 h-full space-y-2 flex flex-col shadow-xl">
              <CardHeader className="flex flex-row justify-between items-center">
                <CardTitle className="text-lg">Student Performance</CardTitle>
              </CardHeader>
            </Card>
            <Card className="w-1/2 h-full space-y-2 flex flex-col shadow-xl">
              <CardHeader className="flex flex-row justify-between items-center">
                <CardTitle className="text-lg">Upcoming Dates</CardTitle>
              </CardHeader>
            </Card>
          </div>
          <Card className="w-full h-full space-y-2 flex flex-col shadow-xl">
            <CardHeader className="flex flex-row justify-between items-center">
              <CardTitle className="text-lg">Class Overview</CardTitle>
            </CardHeader>
          </Card>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;
