import * as React from "react";

import { Bar } from "react-chartjs-2";

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

const data = {
  labels: ["0-19%", "20-39%", "40-59%", "60-79%", "80-100%"],
  datasets: [
    {
      label: "Number of Students",
      data: [10, 20, 30, 40, 25],
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
};

const AdministratorView = () => {
  return (
    <div className="bg-white rounded-3xl flex justify-center items-center m-8 p-8 h-2/3 w-3/4">
      <div className="grid grid-cols-3 grid-rows-2 gap-4 h-full w-full">
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle className="text-lg">
              Global Student Performance
            </CardTitle>
          </CardHeader>
          <div className="flex flex-col justify-center items-center space-y-8 mt-4">
            <CardContent className="flex flex-row justify-around space-x-12 p-0">
              <div className="flex flex-col pl-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">10%</h1>
                <h1 className="text-xs">Pass Rate</h1>
              </div>
              <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
              <div className="flex flex-col pr-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">10%</h1>
                <h1 className="text-xs">Mean</h1>
              </div>
            </CardContent>
            <CardContent className="flex flex-row justify-around space-x-12 p-0">
              <div className="flex flex-col pl-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">10%</h1>
                <h1 className="text-xs">Median</h1>
              </div>
              <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
              <div className="flex flex-col pr-12 justify-center items-center w-28 text-center">
                <h1 className="font-bold text-3xl text-primary-blue">10%</h1>
                <h1 className="text-xs">Mode</h1>
              </div>
            </CardContent>
          </div>
        </Card>
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle className="text-lg">High Performing Classes</CardTitle>
          </CardHeader>
          <div className="flex flex-col pl-7 space-y-4 mt-4">
            <div className="flex flex-row space-x-2">
              <div className="flex flex-col">
                <h2 className="text-md font-normal">
                  <span className="font-bold">CS409</span> — Database and Design
                </h2>
                <h2 className="text-sm font-light w-3/4">
                  <span className="text-green-500 font-bold">91%</span> Mean
                </h2>
              </div>
            </div>
            <div className="flex flex-row space-x-2">
              <div className="flex flex-col">
                <h2 className="text-md font-normal">
                  <span className="font-bold">CS409</span> — Database and Design
                </h2>
                <h2 className="text-sm font-light w-3/4">
                  <span className="text-green-500 font-bold">91%</span> Mean
                </h2>
              </div>
            </div>
            <div className="flex flex-row space-x-2">
              <div className="flex flex-col">
                <h2 className="text-md font-normal">
                  <span className="font-bold">CS409</span> — Database and Design
                </h2>
                <h2 className="text-sm font-light w-3/4">
                  <span className="text-green-500 font-bold">91%</span> Mean
                </h2>
              </div>
            </div>
          </div>
        </Card>
        <Card className="col-span-1 row-span-2 flex flex-col shadow-xl">
          <CardHeader className="flex flex-col justify-start items-start">
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
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle className="text-lg">Low Performing Classes</CardTitle>
          </CardHeader>
          <div className="flex flex-col pl-7 space-y-4">
            <div className="flex flex-row space-x-2">
              <div className="flex flex-col">
                <h2 className="text-md font-normal">
                  <span className="font-bold">CS409</span> — Database and Design
                </h2>
                <h2 className="text-sm font-light w-3/4">
                  <span className="text-red-500 font-bold">19%</span> Mean
                </h2>
              </div>
            </div>
            <div className="flex flex-row space-x-2">
              <div className="flex flex-col">
                <h2 className="text-md font-normal">
                  <span className="font-bold">CS409</span> — Database and Design
                </h2>
                <h2 className="text-sm font-light w-3/4">
                  <span className="text-red-500 font-bold">19%</span> Mean
                </h2>
              </div>
            </div>
            <div className="flex flex-row space-x-2">
              <div className="flex flex-col">
                <h2 className="text-md font-normal">
                  <span className="font-bold">CS409</span> — Database and Design
                </h2>
                <h2 className="text-sm font-light w-3/4">
                  <span className="text-red-500 font-bold">19%</span> Mean
                </h2>
              </div>
            </div>
          </div>
        </Card>
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle className="text-lg">Most Consistent Classes</CardTitle>
          </CardHeader>
          <div className="flex flex-col pl-7 space-y-4">
            <div className="flex flex-row space-x-2">
              <div className="flex flex-col">
                <h2 className="text-md font-normal">
                  <span className="font-bold">CS409</span> — Database and Design
                </h2>
                <h2 className="text-sm font-light w-3/4">
                  <span className="text-green-500 font-bold">1%</span> Standard
                  Deviation
                </h2>
              </div>
            </div>
            <div className="flex flex-row space-x-2">
              <div className="flex flex-col">
                <h2 className="text-md font-normal">
                  <span className="font-bold">CS409</span> — Database and Design
                </h2>
                <h2 className="text-sm font-light w-3/4">
                  <span className="text-green-500 font-bold">1%</span> Standard
                  Deviation
                </h2>
              </div>
            </div>
            <div className="flex flex-row space-x-2">
              <div className="flex flex-col">
                <h2 className="text-md font-normal">
                  <span className="font-bold">CS409</span> — Database and Design
                </h2>
                <h2 className="text-sm font-light w-3/4">
                  <span className="text-green-500 font-bold">1%</span> Standard
                  Deviation
                </h2>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default AdministratorView;
