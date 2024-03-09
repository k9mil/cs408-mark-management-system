import React, { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import { markService } from "@/services/MarkService";
import { userService } from "@/services/UserService";

import { IStatistics } from "@/models/IMark";
import { ILecturer } from "@/models/IUser";

import { useAuth } from "../../../AuthProvider";

import { Bar } from "react-chartjs-2";

import { ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/24/outline";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
} from "chart.js";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/common/Card";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

const LecturerView = () => {
  const { id, getAccessToken } = useAuth();
  const accessToken = getAccessToken();

  const [statistics, setStatistics] = useState<IStatistics>();
  const [globalStatistics, setGlobalStatistics] = useState<IStatistics>();
  const [lecturer, setLecturer] = useState<ILecturer>();
  const [currentSliceStart, setCurrentSliceStart] = useState<number>(0);
  const [currentSliceEnd, setCurrentSliceEnd] = useState<number>(3);

  const data = {
    labels: ["0-39%", "40-49%", "50-59%", "60-69%", "70-100%"],
    datasets: [
      {
        label: "Number of Students",
        data: statistics
          ? [
              statistics.first_bucket,
              statistics.second_bucket,
              statistics.third_bucket,
              statistics.fourth_bucket,
              statistics.fifth_bucket,
            ]
          : [0, 0, 0, 0, 0],
        backgroundColor: [
          "rgba(98, 178, 253, 1)",
          "rgba(155, 223, 196, 1)",
          "rgba(249, 155, 171, 1)",
          "rgba(255, 180, 79, 1)",
          "rgba(159, 151, 247, 1)",
        ],
        borderColor: [
          "rgba(98, 178, 253, 1)",
          "rgba(155, 223, 196, 1)",
          "rgba(249, 155, 171, 1)",
          "rgba(255, 180, 79, 1)",
          "rgba(159, 151, 247, 1)",
        ],
      },
    ],
  };

  const options = {
    maintainAspectRatio: false,
    scale: {
      ticks: {
        precision: 0,
      },
    },
  };

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

  const globalStatisticsData = async () => {
    try {
      if (accessToken) {
        const result = await markService.getGlobalStatistics(accessToken);
        setGlobalStatistics(result);
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
    globalStatisticsData();
    lecturerData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handlePrev = () => {
    if (currentSliceStart > 0) {
      setCurrentSliceStart(currentSliceStart - 3);
      setCurrentSliceEnd(currentSliceEnd - 3);
    }
  };

  const handleNext = () => {
    if (lecturer && currentSliceEnd < lecturer.classes.length) {
      setCurrentSliceStart(currentSliceStart + 3);
      setCurrentSliceEnd(currentSliceEnd + 3);
    }
  };

  return (
    <div className="bg-white rounded-3xl flex justify-center items-center xl:m-8 m-2 2xl:p-6 p-4 2xl:h-2/3 2xl:w-3/4 xl:h-5/6 xl:w-full h-[90%] w-full">
      <div className="grid grid-cols-3 grid-rows-2 gap-3 h-full w-full">
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center p-5">
            <CardTitle className="text-lg">
              Global Student Performance
            </CardTitle>
          </CardHeader>
          <div className="flex flex-col justify-center items-center space-y-8 mt-4">
            <CardContent className="flex flex-row justify-around space-x-12 p-0">
              <div className="flex flex-col pl-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">
                  {globalStatistics ? globalStatistics.pass_rate + "%" : "N/A"}
                </h1>
                <h1 className="text-xs">Pass Rate</h1>
              </div>
              <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
              <div className="flex flex-col pr-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">
                  {globalStatistics ? globalStatistics.mean + "%" : "N/A"}
                </h1>
                <h1 className="text-xs">Mean</h1>
              </div>
            </CardContent>
            <CardContent className="flex flex-row justify-around space-x-12 p-0">
              <div className="flex flex-col pl-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">
                  {globalStatistics ? globalStatistics.median + "%" : "N/A"}
                </h1>
                <h1 className="text-xs">Median</h1>
              </div>
              <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
              <div className="flex flex-col pr-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">
                  {globalStatistics ? globalStatistics.mode + "%" : "N/A"}
                </h1>
                <h1 className="text-xs">Mode</h1>
              </div>
            </CardContent>
          </div>
        </Card>
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center p-5">
            <CardTitle className="text-lg">Your Student Performance</CardTitle>
          </CardHeader>
          {statistics ? (
            <div className="flex flex-col justify-center items-center space-y-8 mt-4">
              <CardContent className="flex flex-row justify-around space-x-12 p-0">
                <div className="flex flex-col pl-12 justify-center items-center w-28 text-center">
                  <h1 className="font-bold text-3xl text-primary-blue">
                    {statistics ? statistics.pass_rate + "%" : null}
                  </h1>
                  <h1 className="text-xs">Pass Rate</h1>
                </div>
                <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                <div className="flex flex-col pr-12 justify-center items-center w-28 text-center">
                  <h1 className="font-bold text-3xl text-primary-blue">
                    {statistics ? statistics.mean + "%" : null}
                  </h1>
                  <h1 className="text-xs">Mean</h1>
                </div>
              </CardContent>
              <CardContent className="flex flex-row justify-around space-x-12 p-0">
                <div className="flex flex-col pl-12 justify-center items-center w-28 text-center">
                  <h1 className="font-bold text-3xl text-primary-blue">
                    {statistics ? statistics.median + "%" : null}
                  </h1>
                  <h1 className="text-xs">Median</h1>
                </div>
                <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                <div className="flex flex-col pr-12 justify-center items-center w-28 text-center">
                  <h1 className="font-bold text-3xl text-primary-blue">
                    {statistics ? statistics.mode + "%" : null}
                  </h1>
                  <h1 className="text-xs">Mode</h1>
                </div>
              </CardContent>
            </div>
          ) : lecturer && lecturer.classes.length ? (
            <h2 className="px-6 font-normal text-sm">
              Ready to upload marks for one of your classes? Head over to the{" "}
              <Link
                to="/upload"
                className="text-blue-400 font-bold hover:underline"
              >
                upload page
              </Link>{" "}
              and get uploading!
            </h2>
          ) : (
            <h2 className="px-6 font-normal text-sm">
              No classes assigned yet. To upload marks, please get assigned to a
              class by{" "}
              <Link
                to="/help"
                className="text-blue-400 font-bold hover:underline"
              >
                contacting an administrator
              </Link>
              .
            </h2>
          )}
        </Card>
        <Card className="col-span-1 row-span-2 flex flex-col shadow-xl">
          <CardHeader className="flex flex-col justify-start items-start p-5">
            <CardTitle className="text-lg">Student Mark Distribution</CardTitle>
            <CardDescription className="font-light">
              This bar graph depicts your uploaded student marks grouped into
              five performance brackets.
            </CardDescription>
          </CardHeader>
          <div className="flex flex-col pl-7 pr-7 mb-7 h-full">
            <Bar data={data} options={options} />
          </div>
        </Card>
        <Card className="col-span-2 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center p-5">
            <CardTitle className="text-lg">Class Overview</CardTitle>
          </CardHeader>
          <div className="flex flex-col px-6">
            <div className="flex flex-row space-x-4 mt-8">
              {lecturer && lecturer.classes.length > 0 ? (
                lecturer.classes
                  .slice(currentSliceStart, currentSliceEnd)
                  .map((class_, index) => (
                    <React.Fragment key={class_.code}>
                      <div className="flex flex-col w-1/3 space-y-2">
                        <h1 className="font-semibold text-base">
                          {class_.code} |{" "}
                          <span className="font-normal"> {class_.name}</span>
                        </h1>
                        {class_.is_uploaded === true ? (
                          <h2 className="text-green-800 font-sm font-bold inline-block rounded-md py-1 px-3 bg-green-100 w-max">
                            Uploaded
                          </h2>
                        ) : (
                          <h2 className="text-red-800 font-sm font-bold inline-block rounded-md py-1 px-3 bg-red-100 w-max">
                            Upload Due
                          </h2>
                        )}
                      </div>
                      {index !== lecturer.classes.slice(0, 3).length - 1 && (
                        <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                      )}
                    </React.Fragment>
                  ))
              ) : (
                <h2 className="font-normal text-sm -mt-6">
                  It seems that you are not assigned to any classes.
                  <Link
                    to="/help"
                    className="text-blue-400 font-bold hover:underline"
                  >
                    {" "}
                    Contact an administrator
                  </Link>{" "}
                  and get assigned to a class!
                </h2>
              )}
            </div>
          </div>
          {lecturer && lecturer.classes.length > 0 ? (
            <div className="flex justify-end items-end h-full w-full p-6">
              <ChevronLeftIcon
                className={`h-6 w-6 ${
                  currentSliceStart === 0
                    ? "text-gray-200"
                    : "hover:cursor-pointer text-black"
                }`}
                onClick={handlePrev}
              />
              <ChevronRightIcon
                className={`h-6 w-6 ${
                  lecturer.classes.length === 0 ||
                  currentSliceEnd >= lecturer.classes.length
                    ? "text-gray-200"
                    : "hover:cursor-pointer text-black"
                }`}
                onClick={handleNext}
              />
            </div>
          ) : null}
        </Card>
      </div>
    </div>
  );
};

export default LecturerView;
