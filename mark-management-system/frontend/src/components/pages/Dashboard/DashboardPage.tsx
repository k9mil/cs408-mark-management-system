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
              <div className="flex flex-col justify-center items-center space-y-8">
                <CardDescription className="flex flex-row justify-around space-x-12">
                  <div className="flex flex-col pl-12 justify-center items-center">
                    <h1 className="font-bold text-3xl text-primary-blue">
                      72%
                    </h1>
                    <h1 className="text-xs">Average</h1>
                  </div>
                  <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                  <div className="flex flex-col pr-12 justify-center items-center">
                    <h1 className="font-bold text-3xl text-primary-blue">
                      44%
                    </h1>
                    <h1 className="text-xs">Mean</h1>
                  </div>
                </CardDescription>
                <CardDescription className="flex flex-row justify-around space-x-12">
                  <div className="flex flex-col pl-12 justify-center items-center">
                    <h1 className="font-bold text-3xl text-primary-blue">
                      17%
                    </h1>
                    <h1 className="text-xs">Median</h1>
                  </div>
                  <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                  <div className="flex flex-col pr-12 justify-center items-center">
                    <h1 className="font-bold text-3xl text-primary-blue">
                      62%
                    </h1>
                    <h1 className="text-xs">Mode</h1>
                  </div>
                </CardDescription>
              </div>
            </Card>
            <Card className="w-1/2 h-full space-y-2 flex flex-col shadow-xl">
              <CardHeader className="flex flex-row justify-between items-center">
                <CardTitle className="text-lg">Upcoming Dates</CardTitle>
              </CardHeader>
              <div className="flex flex-col pl-7 space-y-12">
                <div className="flex flex-row space-x-2">
                  <span className="flex h-2 w-2 translate-y-2 rounded-full bg-primary-blue" />
                  <div className="flex flex-col">
                    <h2 className="text-md font-semibold">CS408 Examination</h2>
                    <h2 className="text-sm font-light">
                      in 3 days, at: John Anderson Room 325
                    </h2>
                  </div>
                </div>
                <div className="flex flex-row space-x-2">
                  <span className="flex h-2 w-2 translate-y-2 rounded-full bg-primary-blue" />
                  <div className="flex flex-col">
                    <h2 className="text-md font-semibold">CS217 Examination</h2>
                    <h2 className="text-sm font-light">
                      in 5 days, at: Royal College Room 557
                    </h2>
                  </div>
                </div>
              </div>
            </Card>
          </div>
          <Card className="w-full h-full space-y-6 flex flex-col shadow-xl">
            <CardHeader className="flex flex-row justify-between items-center">
              <CardTitle className="text-lg">Class Overview</CardTitle>
            </CardHeader>
            <div className="flex flex-col px-7">
              <div className="flex flex-row space-x-4">
                <div className="flex flex-col">
                  <h1 className="font-semibold text-base">
                    CS408 |{" "}
                    <span className="font-normal">Individual Project</span>
                  </h1>
                  <h2 className="text-red-500 font-sm font-normal italic">
                    Upload Due
                  </h2>
                </div>
                <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                <div className="flex flex-col">
                  <h1 className="font-semibold text-base">
                    CS426 |{" "}
                    <span className="font-normal">Human-Centred Security</span>
                  </h1>
                  <h2 className="text-red-500 font-sm font-normal italic">
                    Upload Due
                  </h2>
                </div>
                <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                <div className="flex flex-col">
                  <h1 className="font-semibold text-base">
                    CS412 |{" "}
                    <span className="font-normal">
                      Information Access and Mining
                    </span>
                  </h1>
                  <h2 className="text-green-500 font-sm font-normal italic">
                    Uploaded
                  </h2>
                </div>
              </div>
            </div>
            <h2 className="text-sm text-black font-semibold flex self-end mr-8 pt-4">
              “The place of useful learning.”
            </h2>
          </Card>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;
