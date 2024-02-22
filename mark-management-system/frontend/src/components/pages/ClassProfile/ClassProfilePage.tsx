import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import Sidebar from "../../common/Sidebar";

import { classService } from "@/services/ClassService";
import { markService } from "@/services/MarkService";

import { IClass } from "@/models/IClass";
import { IUserDropdown } from "@/models/IUser";
import { IMarkRow } from "@/models/IMark";

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
  const [classData, setClassData] = useState<IClass[]>([]);
  const [markData, setMarkData] = useState<IMarkRow[]>([]);

  const accessToken = getAccessToken();

  useEffect(() => {
    document.title = "Mark Management System | Class Profile";

    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

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
            console.log(result);
          }
        } catch (error) {
          console.error(error);
        }
      };

      retrieveMarksForClasses();
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
                    This area will fill with information once a user has been
                    picked.
                  </h2>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClassProfilePage;
