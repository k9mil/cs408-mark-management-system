import * as React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import DashboardPage from "./components/pages/Dashboard/DashboardPage";
import MarksPage from "./components/pages/Marks/MarksPage";
import LoginPage from "./components/pages/Login/LoginPage";
import ClassesPage from "./components/pages/Classes/ClassesPage";
import StudentsPage from "./components/pages/Students/StudentsPage";
import HelpPage from "./components/pages/Help/HelpPage";
import SettingsPage from "./components/pages/Settings/SettingsPage";

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
      path: "/marks",
      element: <MarksPage />,
    },
    {
      path: "/classes",
      element: <ClassesPage />,
    },
    {
      path: "/students",
      element: <StudentsPage />,
    },
    {
      path: "/help",
      element: <HelpPage />,
    },
    {
      path: "/settings",
      element: <SettingsPage />,
    },
  ]);

  return <RouterProvider router={router} />;
};

export default Routes;
