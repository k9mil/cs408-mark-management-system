import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "@/AuthProvider";

import Sidebar from "@/components/common/Sidebar";

import { StudentsDataTable } from "./StudentsDataTable";
import { StudentColumns } from "./StudentsColumns";

import { markService } from "@/services/MarkService";

import { IMarkRow } from "@/models/IMark";

const StudentsPage = () => {
  const navigate = useNavigate();
  const { isLecturer, isAuthenticated, getAccessToken } = useAuth();

  const [details, setDetails] = useState<IMarkRow[]>([]);

  const accessToken = getAccessToken();

  useEffect(() => {
    document.title = "Mark Management System | Graded Students";

    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  const marksData = async () => {
    try {
      if (accessToken) {
        if (isLecturer) {
          const result = await markService.getStudentMarks(accessToken);
          setDetails(result);
        }
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    marksData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl">
        <div className="m-8 flex flex-col space-y-4">
          <div className="flex 2xl:flex-col xl:flex-row 2xl:space-y-1 xl:space-x-2 2xl:space-x-0 xl:items-center 2xl:items-start">
            <h1 className="text-3xl font-bold">Graded Students</h1>
            <h2 className="text-gray-400">
              View the students that you have uploaded marks for
            </h2>
          </div>
          <StudentsDataTable
            columns={StudentColumns}
            data={details}
            accessToken={accessToken}
            marksData={marksData}
          />
        </div>
      </div>
    </div>
  );
};

export default StudentsPage;
