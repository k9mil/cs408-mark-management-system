import React, { useEffect } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/common/Card";

import Sidebar from "../../common/Sidebar";

const HelpPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    document.title = "Mark Management System | Help & Support";

    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center">
        <Card className="w-1/2 h-1/2 space-y-2 p-8 flex flex-col">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle>Help & Support</CardTitle>
          </CardHeader>
          <div className="flex flex-col space-y-4">
            <CardDescription className="mx-6">
              We're here to help! You can find information boxes throughout the
              site, which will aid you in particular tasks, such as Marks
              Uploading and the constraints it has or general information about
              the system.
            </CardDescription>
            <CardDescription className="mx-6">
              However — if you need additional help with regards to the service,
              contact us by email, phone or alternatively our IT Support Portal:
            </CardDescription>
            <CardDescription className="mx-6">
              <div className="flex flex-row space-x-2">
                <h2 className="font-bold">Email:</h2>{" "}
                <span className="underline text-blue-400">
                  help@strath.ac.uk
                </span>
              </div>
              <div className="flex flex-row space-x-2">
                <h2 className="font-bold">Telephone:</h2>{" "}
                <span className="underline">+44 (0)141 548 4444</span>
              </div>
              <div className="flex flex-row space-x-2">
                <h2 className="font-bold">IT Support Portal:</h2>{" "}
                <span className="text-blue-400 underline">
                  https://helpdesk.strath.ac.uk/support/home
                </span>
              </div>
            </CardDescription>
            <CardDescription className="mx-6">
              For even more points of support, visit:{" "}
              <span className="text-blue-400 underline">
                https://www.strath.ac.uk/professionalservices/informationservices/contact/
              </span>
            </CardDescription>
            <CardDescription className="mx-6">
              Thanks for visiting our help section — we're always here to ensure
              your experience is smooth and enjoyable!
            </CardDescription>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default HelpPage;
