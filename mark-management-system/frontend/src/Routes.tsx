import * as React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

// import DashboardPage from "./components/DashboardPage";
import MarksPage from "./components/pages/Marks/MarksPage";
// import StudentsPage from "./components/StudentsPage";
// import ReportsPage from "./components/ReportsPage";
// import UserManagementPage from "./components/UserManagementPage";
// import HelpPage from "./components/HelpPage";
// import SettingsPage from "./components/SettingsPage";

const Routes = () => {
  const router = createBrowserRouter([
    {
      path: "/",
      //   element: <DashboardPage />,
      children: [
        {
          path: "/marks",
          element: <MarksPage />,
        },
        // {
        //   path: "/students",
        //   element: <StudentsPage />,
        // },
        // {
        //   path: "/reports",
        //   element: <ReportsPage />,
        // },
        // {
        //   path: "/user_management",
        //   element: <UserManagementPage />,
        // },
        // {
        //   path: "/help",
        //   element: <HelpPage />,
        // },
        // {
        //   path: "/settings",
        //   element: <SettingsPage />,
        // },
      ],
    },
  ]);

  return <RouterProvider router={router} />;
};

export default Routes;
