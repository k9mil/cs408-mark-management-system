import React, { useState, useEffect } from "react";

import { Bar } from "react-chartjs-2";

import { useAuth } from "../../../AuthProvider";

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

import { markService } from "@/services/MarkService";
import { IMarkMetrics, IStatistics } from "@/models/IMark";
import { classService } from "@/services/ClassService";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

const AdministratorView = () => {
  const { getAccessToken } = useAuth();
  const accessToken = getAccessToken();

  const [globalStatistics, setGlobalStatistics] = useState<IStatistics>();
  const [classMetrics, setClassMetrics] = useState<IMarkMetrics>();

  const data = {
    labels: ["0-19%", "20-39%", "40-59%", "60-79%", "80-100%"],
    datasets: [
      {
        label: "Number of Students",
        data: globalStatistics
          ? [
              globalStatistics.first_bucket,
              globalStatistics.second_bucket,
              globalStatistics.third_bucket,
              globalStatistics.fourth_bucket,
              globalStatistics.fifth_bucket,
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

  const globalMetricsData = async () => {
    try {
      if (accessToken) {
        const result = await classService.getClassMetrics(accessToken);
        result.highest_performing_classes.reverse();
        setClassMetrics(result);
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    document.title = "Mark Management System | Dashboard";

    globalStatisticsData();
    globalMetricsData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="bg-white rounded-3xl flex justify-center items-center m-8 p-6 2xl:h-2/3 2xl:w-3/4 xl:h-4/5 xl:w-full">
      <div className="grid grid-cols-3 grid-rows-2 gap-3 h-full w-full">
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center  p-5">
            <CardTitle className="text-lg">
              Global Student Performance
            </CardTitle>
          </CardHeader>
          <div className="flex flex-col justify-center items-center space-y-8 mt-4">
            <CardContent className="flex flex-row justify-around space-x-12 p-0">
              <div className="flex flex-col pl-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">
                  {globalStatistics ? globalStatistics.pass_rate + "%" : null}
                </h1>
                <h1 className="text-xs">Pass Rate</h1>
              </div>
              <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
              <div className="flex flex-col pr-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">
                  {globalStatistics ? globalStatistics.mean + "%" : null}
                </h1>
                <h1 className="text-xs">Mean</h1>
              </div>
            </CardContent>
            <CardContent className="flex flex-row justify-around space-x-12 p-0">
              <div className="flex flex-col pl-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">
                  {globalStatistics ? globalStatistics.median + "%" : null}
                </h1>
                <h1 className="text-xs">Median</h1>
              </div>
              <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
              <div className="flex flex-col pr-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">
                  {globalStatistics ? globalStatistics.mode + "%" : null}
                </h1>
                <h1 className="text-xs">Mode</h1>
              </div>
            </CardContent>
          </div>
        </Card>
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center p-5">
            <CardTitle className="text-lg">High Performing Classes</CardTitle>
          </CardHeader>
          <div className="flex flex-col pl-7 space-y-4">
            {classMetrics
              ? classMetrics.highest_performing_classes.map((class_) => (
                  <div className="flex flex-row space-x-2" key={class_.code}>
                    <div className="flex flex-col">
                      <h2 className="text-md font-normal max-w-sm">
                        <span className="font-bold">{class_.code}</span> —{" "}
                        <span className="pr-4 text-sm">{class_.name}</span>
                      </h2>
                      <h2 className="text-sm font-light w-3/4">
                        <span className="text-green-500 font-bold">
                          {class_.mean}%
                        </span>{" "}
                        Mean
                      </h2>
                    </div>
                  </div>
                ))
              : null}
          </div>
        </Card>
        <Card className="col-span-1 row-span-2 flex flex-col shadow-xl">
          <CardHeader className="flex flex-col justify-start items-start p-5">
            <CardTitle className="text-lg">Student Mark Distribution</CardTitle>
            <CardDescription className="font-light">
              This bar graph depicts all student marks grouped into five
              performance brackets.
            </CardDescription>
          </CardHeader>
          <div className="flex flex-col pl-7 pr-7 mb-7 h-full">
            <Bar data={data} options={options} />
          </div>
        </Card>
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center p-5">
            <CardTitle className="text-lg">Low Performing Classes</CardTitle>
          </CardHeader>
          <div className="flex flex-col pl-7 space-y-4">
            {classMetrics
              ? classMetrics.lowest_performing_classes.map((class_) => (
                  <div className="flex flex-row space-x-2" key={class_.code}>
                    <div className="flex flex-col">
                      <h2 className="text-md font-normal max-w-sm">
                        <span className="font-bold">{class_.code}</span> —{" "}
                        <span className="pr-4 text-sm">{class_.name}</span>
                      </h2>
                      <h2 className="text-sm font-light w-3/4">
                        <span className="text-red-500 font-bold">
                          {class_.mean}%
                        </span>{" "}
                        Mean
                      </h2>
                    </div>
                  </div>
                ))
              : null}
          </div>
        </Card>
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center p-5">
            <CardTitle className="text-lg">Most Consistent Classes</CardTitle>
          </CardHeader>
          <div className="flex flex-col pl-7 space-y-4">
            {classMetrics
              ? classMetrics.most_consistent_classes.map((class_) => (
                  <div className="flex flex-row space-x-2" key={class_.code}>
                    <div className="flex flex-col">
                      <h2 className="text-md font-normal max-w-sm">
                        <span className="font-bold">{class_.code}</span> —{" "}
                        <span className="pr-4 text-sm">{class_.name}</span>
                      </h2>
                      <h2 className="text-sm font-light">
                        <span className="text-green-500 font-bold">
                          {class_.stdev}%
                        </span>{" "}
                        Standard Deviation
                      </h2>
                    </div>
                  </div>
                ))
              : null}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default AdministratorView;
