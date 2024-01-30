import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/common/Card";

import Sidebar from "../../common/Sidebar";

import { markService } from "@/services/MarkService";
import { userService } from "@/services/UserService";

import { IStatistics } from "@/models/IMark";
import { ILecturer } from "@/models/IUser";
import { IClass, IClassUploaded } from "@/models/IClass";

const DashboardPage = () => {
  const navigate = useNavigate();
  const { id, isAuthenticated, getAccessToken } = useAuth();

  const [statistics, setStatistics] = useState<IStatistics>();
  const [lecturer, setLecturer] = useState<ILecturer>();

  const accessToken = getAccessToken();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  const statisticsData = async () => {
    try {
      if (accessToken) {
        const result = await markService.getStatistics(accessToken);
        setStatistics(result);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const lecturerData = async () => {
    try {
      if (accessToken) {
        const result = await userService.getLecturer(id, accessToken);
        setLecturer(result);
        console.log(result);
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    document.title = "Mark Management System | Dashboard";

    statisticsData();
    lecturerData();
  }, []);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center">
        <Card className="w-1/2 h-4/6 space-y-4 p-8 flex flex-col">
          <div className="flex flex-row space-x-8 h-full">
            <Card className="w-1/2 h-full space-y-2 flex flex-col shadow-xl">
              <CardHeader className="flex flex-row justify-between items-center">
                <CardTitle className="text-lg">Student Performance</CardTitle>
              </CardHeader>
              {statistics ? (
                <div className="flex flex-col justify-center items-center space-y-8">
                  <CardDescription className="flex flex-row justify-around space-x-12">
                    <div className="flex flex-col pl-12 justify-center items-center">
                      <h1 className="font-bold text-3xl text-primary-blue">
                        {statistics ? statistics.pass_rate + "%" : null}
                      </h1>
                      <h1 className="text-xs">Pass Rate</h1>
                    </div>
                    <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                    <div className="flex flex-col pr-12 justify-center items-center">
                      <h1 className="font-bold text-3xl text-primary-blue">
                        {statistics ? statistics.mean + "%" : null}
                      </h1>
                      <h1 className="text-xs">Mean</h1>
                    </div>
                  </CardDescription>
                  <CardDescription className="flex flex-row justify-around space-x-12">
                    <div className="flex flex-col pl-12 justify-center items-center">
                      <h1 className="font-bold text-3xl text-primary-blue">
                        {statistics ? statistics.median + "%" : null}
                      </h1>
                      <h1 className="text-xs">Median</h1>
                    </div>
                    <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                    <div className="flex flex-col pr-12 justify-center items-center">
                      <h1 className="font-bold text-3xl text-primary-blue">
                        {statistics ? statistics.mode + "%" : null}
                      </h1>
                      <h1 className="text-xs">Mode</h1>
                    </div>
                  </CardDescription>
                </div>
              ) : (
                <h2 className="pl-7 font-normal text-sm">
                  You haven't uploaded any marks yet.
                </h2>
              )}
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
                {lecturer && lecturer.classes.length > 0 ? (
                  lecturer.classes
                    .slice(0, 3)
                    .map((class_: IClassUploaded, index: number) => (
                      <>
                        <div className="flex flex-col w-1/3">
                          <h1 className="font-semibold text-base">
                            {class_.code} |
                            <span className="font-normal"> {class_.name}</span>
                          </h1>
                          {class_.is_uploaded === true ? (
                            <h2 className="text-green-500 font-sm font-normal italic">
                              Uploaded
                            </h2>
                          ) : (
                            <h2 className="text-red-500 font-sm font-normal italic">
                              Upload Due
                            </h2>
                          )}
                        </div>
                        {index !== lecturer.classes.slice(0, 3).length - 1 && (
                          <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                        )}
                      </>
                    ))
                ) : (
                  <h2 className="font-normal text-sm">
                    You are not assigned to any classes.
                  </h2>
                )}
              </div>
            </div>
            {lecturer && lecturer.classes.length > 0 ? (
              <h2 className="text-sm text-black font-semibold flex self-end mr-8 relative -bottom-8">
                “The place of useful learning.”
              </h2>
            ) : null}
          </Card>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;
