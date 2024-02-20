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
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center space-x-2">
        <Card className="2xl:w-1/2 xl:w-1/2 2xl:h-1/2 x:h-3/4 space-y-2 p-4 flex flex-col">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle>Help & Support</CardTitle>
          </CardHeader>
          <div className="flex flex-col space-y-4">
            <CardContent className="mx-6 text-sm text-muted-foreground p-0">
              We're here to help! You can find information boxes throughout the
              site, which will aid you in particular tasks, such as Marks
              Uploading and the constraints it has or general information about
              the system.
            </CardContent>
            <CardContent className="mx-6 text-sm text-muted-foreground p-0">
              However — if you need additional help with regards to the service,
              contact us by email, phone or alternatively our IT Support Portal:
            </CardContent>
            <CardContent className="mx-6 text-sm text-muted-foreground p-0">
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
            </CardContent>
            <CardContent className="mx-6 text-sm text-muted-foreground p-0">
              For even more points of support, visit:{" "}
              <span className="text-blue-400 underline break-all">
                https://www.strath.ac.uk/professionalservices/informationservices/contact/
              </span>
            </CardContent>
            <CardContent className="mx-6 text-sm text-muted-foreground p-0">
              Thanks for visiting our help section — we're always here to ensure
              your experience is smooth and enjoyable!
            </CardContent>
          </div>
        </Card>
        <Card className="2xl:w-1/3 xl:w-1/3 2xl:h-1/2 x:h-3/4 space-y-2 p-4 flex flex-col">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle>Conversion Formats</CardTitle>
          </CardHeader>
          <div className="flex flex-col space-y-4">
            <CardContent className="mx-6 text-sm text-muted-foreground p-0">
              If you are wanting to convert from the MyPlace format to the MMS
              format, see below for the required format:
            </CardContent>
            <CardContent className="mx-6 text-sm font-semibold text-muted-foreground p-0">
              CLASS_CODE, DATE, REG_NO, CLASS_TOTAL, OVERRIDE_MARK
            </CardContent>
            <CardContent className="mx-6 text-sm text-muted-foreground p-0">
              (e.g., CS123,01/01/2024,abc12345,45,50).
            </CardContent>
            <CardContent className="mx-6 text-sm text-muted-foreground p-0">
              If you are wanting to convert from the MMS format to the Pegasus
              format, see below for the required format:
            </CardContent>
            <CardContent className="mx-6 text-sm font-semibold text-muted-foreground p-0">
              CLASS_CODE, REG_NO, MARK, MARK_CODE, STUDENT_NAME, COURSE, DEGREE,
              DEGREE_CODE, RESULT
            </CardContent>
            <CardContent className="mx-6 text-sm text-muted-foreground p-0">
              (e.g., CS123,abc12345,FILL IN,John Doe,Computer
              Science,BSc,0403/2,FILL IN).
            </CardContent>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default HelpPage;
