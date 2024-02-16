import * as React from "react";

import { createBrowserRouter, RouterProvider } from "react-router-dom";

import DashboardPage from "./components/pages/Dashboard/DashboardPage";
import ConvertPage from "./components/pages/Convert/ConvertPage";
import UploadPage from "./components/pages/Upload/UploadPage";
import LoginPage from "./components/pages/Login/LoginPage";
import ClassesPage from "./components/pages/Classes/ClassesPage";
import StudentsPage from "./components/pages/Students/StudentsPage";
import StudentProfilePage from "./components/pages/StudentProfile/StudentProfilePage";
import LecturersPage from "./components/pages/Lecturers/LecturersPage";
import HelpPage from "./components/pages/Help/HelpPage";
import SettingsPage from "./components/pages/Settings/SettingsPage";

import ErrorPage from "./components/pages/Error/ErrorPage_404";

const Routes = () => {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <LoginPage />,
    },
    {
      path: "/dashboard",
      element: <DashboardPage />,
    },
    {
      path: "/convert",
      element: <ConvertPage />,
    },
    {
      path: "/upload",
      element: <UploadPage />,
    },
    {
      path: "/classes",
      element: <ClassesPage />,
    },
    {
      path: "/graded-students",
      element: <StudentsPage />,
    },
    {
      path: "/student-profile",
      element: <StudentProfilePage />,
    },
    {
      path: "/lecturers",
      element: <LecturersPage />,
    },
    {
      path: "/help",
      element: <HelpPage />,
    },
    {
      path: "/settings",
      element: <SettingsPage />,
    },
    {
      path: "*",
      element: <ErrorPage />,
    },
  ]);

  return <RouterProvider router={router} />;
};

export default Routes;
