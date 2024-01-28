import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import Sidebar from "../../common/Sidebar";

import { StudentsDataTable } from "./StudentsDataTable";
import { StudentColumns } from "./StudentsColumns";

import { markService } from "../../../services/MarkService";

import { IMarkRow } from "../../../models/IMark";

const StudentsPage = () => {
  const navigate = useNavigate();
  const { isLecturer, isAuthenticated, getAccessToken } = useAuth();

  const [details, setDetails] = useState<IMarkRow[]>([]);

  const accessToken = getAccessToken();

  useEffect(() => {
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
  }, []);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl">
        <div className="m-8 flex flex-col space-y-4">
          <div className="flex flex-col space-y-4">
            <h1 className="text-3xl font-bold">Students</h1>
            <h2 className="text-gray-400">
              View the students that you have uploaded marks for
            </h2>
          </div>
          <StudentsDataTable
            columns={StudentColumns}
            data={details}
            marksData={marksData}
            accessToken={accessToken}
          />
        </div>
      </div>
    </div>
  );
};

export default StudentsPage;
