import React, { useEffect } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/common/Card";

import Sidebar from "../../common/Sidebar";

const ClassProfilePage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    document.title = "Mark Management System | Class Profile";

    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center space-x-2"></div>
    </div>
  );
};

export default ClassProfilePage;
