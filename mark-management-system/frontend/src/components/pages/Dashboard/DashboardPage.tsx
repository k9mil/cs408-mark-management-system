import React, { useEffect } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import Sidebar from "../../common/Sidebar";

import AdministratorView from "./AdministratorView";
import LecturerView from "./LecturerView";
import NoRoleView from "./NoRoleView";

const DashboardPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, isAdmin, isLecturer } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] bg-slate-100 rounded-3xl m-auto">
        <div className="flex justify-center items-center h-full w-full">
          {isLecturer && !isAdmin ? (
            <LecturerView />
          ) : isAdmin ? (
            <AdministratorView />
          ) : (
            <NoRoleView />
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
