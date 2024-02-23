import React, { useEffect, useState } from "react";

import { useNavigate, Link } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import Sidebar from "../../common/Sidebar";

import { markService } from "@/services/MarkService";
import { userService } from "@/services/UserService";

import { IStatistics } from "@/models/IMark";
import { ILecturer } from "@/models/IUser";
import { IClassUploaded } from "@/models/IClass";
import AdministratorView from "./AdministratorView";
import LecturerView from "./LecturerView";

const DashboardPage = () => {
  const navigate = useNavigate();
  const { id, isAuthenticated, getAccessToken, isAdmin, isLecturer } =
    useAuth();

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
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    document.title = "Mark Management System | Dashboard";

    statisticsData();
    lecturerData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] bg-slate-100 rounded-3xl m-auto">
        <div className="flex justify-center items-center h-full w-full">
          <LecturerView />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
