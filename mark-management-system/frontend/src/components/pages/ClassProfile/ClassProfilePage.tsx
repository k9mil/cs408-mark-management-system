import React, { useEffect, useState } from "react";

import { useNavigate, Link } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import Sidebar from "../../common/Sidebar";

import { classService } from "@/services/ClassService";
import { markService } from "@/services/MarkService";

import { IClass } from "@/models/IClass";
import { IUserDropdown } from "@/models/IUser";
import { IMarkRow, IStatistics } from "@/models/IMark";

import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/components/common/Card";

import ClassProfileDropdown from "./ClassProfileDropdown";
import ClassProfileDataTable from "./ClassProfileDataTable";
import { ClassProfileColumns } from "../Classes/ClassesColumns";

const ClassProfilePage = () => {
  const navigate = useNavigate();
  const { isLecturer, isAdmin, isAuthenticated, getAccessToken } = useAuth();

  const [classList, setClassList] = React.useState<IUserDropdown[] | null>(
    null
  );

  const [classOpen, setClassOpen] = React.useState<boolean>(false);
  const [class_, setClass] = React.useState<string>("");
  const [currentClass, setCurrentClass] = useState<IClass>();
  const [classData, setClassData] = useState<IClass[]>([]);
  const [markData, setMarkData] = useState<IMarkRow[]>([]);
  const [classStatistics, setClassStatistics] = useState<IStatistics>();

  const accessToken = getAccessToken();

  useEffect(() => {
    document.title = "Mark Management System | Class Profile";

    if (!isAuthenticated || (!isAdmin && !isLecturer)) {
      navigate("/");
    }
  }, [navigate, isAuthenticated, isAdmin, isLecturer]);

  const retrieveClassData = async () => {
    try {
      if (accessToken) {
        if (isLecturer || isAdmin) {
          const result = await classService.getClasses(accessToken);
          setClassData(result);
        }
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    if (class_ !== "") {
      const retrieveMarksForClasses = async () => {
        try {
          if (accessToken) {
            const result = await markService.getMarksForClass(
              class_,
              accessToken
            );

            setMarkData(result);
          }
        } catch (error) {
          console.error(error);
        }
      };

      const retrieveClassStatistics = async () => {
        try {
          if (accessToken) {
            const result = await classService.getClassStatistics(
              class_,
              accessToken
            );

            setClassStatistics(result);
          }
        } catch (error) {
          console.error(error);
        }
      };

      retrieveMarksForClasses();
      retrieveClassStatistics();
    }
  }, [class_, accessToken]);

  useEffect(() => {
    retrieveClassData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (classData && Array.isArray(classData)) {
      const mappedClasses = classData.map((class_: IClass) => ({
        value: class_.code,
        label: class_.code,
      }));

      setClassList(mappedClasses);
    }
  }, [classData]);

  useEffect(() => {
    const foundClass = classData.find((c) => c.code === class_);

    setCurrentClass(foundClass);
  }, [class_, classData]);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl">
        <div className="mt-8 ml-8 mr-8 flex flex-col space-y-4">
          <div className="flex 2xl:flex-col xl:flex-row 2xl:space-y-1 xl:space-x-2 2xl:space-x-0 xl:items-center 2xl:items-start">
            <h1 className="text-3xl font-bold">Class Profile</h1>
            <h2 className="text-gray-400">
              Enter a class code to view all marks recorded for that class
            </h2>
          </div>
        </div>
        <div className="flex flex-row w-full h-[80vh]">
          <div
            className={`flex flex-col space-y-1 m-8 ${
              class_ && class_ !== "" ? "w-1/2" : "w-full"
            }`}
          >
            <div className="flex flex-row justify-between py-2">
              <div className="flex items-center w-1/5">
                {classList !== null && classList.length !== 0 ? (
                  <ClassProfileDropdown
                    class_={class_}
                    classOpen={classOpen}
                    setClass={setClass}
                    setClassOpen={setClassOpen}
                    classList={classList}
                  />
                ) : null}
              </div>
            </div>
            {class_ && class_ !== "" && markData ? (
              <ClassProfileDataTable
                columns={ClassProfileColumns}
                data={markData}
                accessToken={accessToken}
              />
            ) : (
              <div className="flex flex-col justify-center items-center m-auto h-full space-y-4">
                <div className="w-96 h-96">
                  <img src="/empty_state.svg" alt="No data found" />
                </div>
                <div className="space-y-2 flex flex-col justify-center items-center">
                  <h1 className="font-bold text-2xl">No data found</h1>
                  <h2 className="font-light text-md">
                    This area will fill with information once a class has been
                    picked.
                  </h2>
                </div>
              </div>
            )}
          </div>
          {class_ && class_ !== "" ? (
            <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
          ) : null}
          {class_ && class_ !== "" ? (
            <div className="flex flex-col justify-center items-center w-2/5 m-auto 2xl:space-y-8 xl:space-y-4">
              <Card className="w-full h-1/2 space-y-2 flex justify-center flex-col shadow-xl 2xl:p-8 xl:p-4">
                <CardHeader className="flex flex-row justify-start items-start p-0">
                  <CardTitle className="2xl:text-2xl xl:text-xl font-bold mb-6">
                    Class Details
                  </CardTitle>
                </CardHeader>
                {classData && currentClass ? (
                  <div className="flex flex-row w-full justify-between items-center">
                    <div className="flex flex-col space-y-6 w-2/3">
                      <div className="flex flex-col space-y-2">
                        <div className="flex flex-row space-x-2 w-full">
                          <h2 className="2xl:text-base xl:text-sm font-semibold">
                            Class Name:
                          </h2>
                          <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                            {currentClass.name}
                          </h2>
                        </div>
                        <div className="flex flex-row space-x-2 w-full">
                          <h2 className="2xl:text-base xl:text-sm font-semibold">
                            Class Code:
                          </h2>
                          <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                            {currentClass.code}
                          </h2>
                        </div>
                        <div className="flex flex-row space-x-2 w-full">
                          <h2 className="2xl:text-base xl:text-sm font-semibold">
                            Credit:
                          </h2>
                          <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                            {currentClass.credit}
                          </h2>
                        </div>
                        <div className="flex flex-row space-x-2 w-full">
                          <h2 className="2xl:text-base xl:text-sm font-semibold">
                            Credit Level:
                          </h2>
                          <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                            {currentClass.credit_level}
                          </h2>
                        </div>
                      </div>
                    </div>
                    {classStatistics ? (
                      <div className="flex flex-col space-y-8 w-1/3">
                        <CardContent className="flex flex-row space-x-4 justify-around p-0 mr-4">
                          <div className="flex flex-col justify-center items-center w-16 text-center">
                            <h1 className="font-bold 2xl:text-3xl xl:text-xl text-primary-blue">
                              {classStatistics.mean === -1
                                ? "N/A"
                                : `${classStatistics.mean}%`}
                            </h1>
                            <h1 className="text-xs 2xl:inline">Mean</h1>
                          </div>
                          <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                          <div className="flex flex-col justify-center items-center w-16 text-center">
                            <h1 className="font-bold 2xl:text-3xl xl:text-xl text-primary-blue">
                              {classStatistics.mode === -1
                                ? "N/A"
                                : `${classStatistics.mode}%`}
                            </h1>
                            <h1 className="text-xs">Mode</h1>
                          </div>
                        </CardContent>
                        <CardContent className="space-x-4 flex flex-row justify-around p-0 mr-4">
                          <div className="flex flex-col justify-center items-center w-16 text-center">
                            <h1 className="font-bold 2xl:text-3xl xl:text-xl text-primary-blue">
                              {classStatistics.median === -1
                                ? "N/A"
                                : `${classStatistics.median}%`}
                            </h1>
                            <h1 className="text-xs">Median</h1>
                          </div>
                          <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                          <div className="flex flex-col justify-center items-center w-16 text-center">
                            <h1 className="font-bold 2xl:text-3xl xl:text-xl text-primary-blue">
                              {classStatistics.pass_rate === -1
                                ? "N/A"
                                : `${classStatistics.pass_rate}%`}
                            </h1>
                            <h1 className="text-xs 2xl:inline">Pass R.</h1>
                          </div>
                        </CardContent>
                      </div>
                    ) : null}
                  </div>
                ) : (
                  <h2 className="text-base font-regular">
                    It seems like there are no student details available at the
                    moment. If you are expecting to see something here,{" "}
                    <Link
                      to="/help"
                      className="text-blue-400 font-bold hover:underline"
                    >
                      contact an administrator
                    </Link>
                    .
                  </h2>
                )}
              </Card>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default ClassProfilePage;
