import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import Sidebar from "../../common/Sidebar";

import { userService } from "@/services/UserService";

import { ILecturer } from "@/models/IUser";

import { LecturerColumns } from "./LecturersColumn";

import LecturersDataTable from "./LecturersDataTable";

const LecturersPage = () => {
  const navigate = useNavigate();
  const { isAdmin, isAuthenticated, getAccessToken } = useAuth();

  const [lecturers, setLecturers] = useState<ILecturer[]>([]);

  const accessToken = getAccessToken();

  useEffect(() => {
    document.title = "Mark Management System | Lecturers";

    if (!isAuthenticated || !isAdmin) {
      navigate("/");
    }
  }, [navigate, isAuthenticated, isAdmin]);

  const lecturersData = async () => {
    try {
      if (accessToken) {
        if (isAdmin) {
          const result = await userService.getLecturers(accessToken);
          setLecturers(result);
        }
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    lecturersData();
  }, []);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl">
        <div className="m-8 flex flex-col space-y-4">
          <div className="flex flex-col space-y-4">
            <h1 className="text-3xl font-bold">Lecturers</h1>
            <h2 className="text-gray-400">
              View a list of lecturers in the system
            </h2>
          </div>
          <LecturersDataTable
            columns={LecturerColumns}
            data={lecturers}
            accessToken={accessToken}
          />
        </div>
      </div>
    </div>
  );
};

export default LecturersPage;
