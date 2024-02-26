import React, { useEffect } from "react";

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
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/common/Card";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

const NoRoleView = () => {
  const data = {
    labels: ["0-19%", "20-39%", "40-59%", "60-79%", "80-100%"],
    datasets: [
      {
        label: "Number of Students",
        data: [0, 0, 0, 0, 0],
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

  useEffect(() => {
    document.title = "Mark Management System | Dashboard";
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="bg-white rounded-3xl flex justify-center items-center xl:m-8 m-2 2xl:p-6 p-4 2xl:h-2/3 2xl:w-3/4 xl:h-5/6 xl:w-full h-[90%] w-full">
      <div className="grid grid-cols-3 grid-rows-2 gap-4 h-full w-full">
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle className="text-lg">
              Global Student Performance
            </CardTitle>
          </CardHeader>
          <h2 className="px-6 font-normal text-sm">
            No roles assigned. To be able see Global Student Performance, please
            reach out to the administrator team to get a role.
          </h2>
        </Card>
        <Card className="col-span-1 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle className="text-lg">Your Student Performance</CardTitle>
          </CardHeader>
          <h2 className="px-6 font-normal text-sm">
            No roles assigned. To be able to upload marks, please reach out to
            the administrator team to provide you with a role to get uploading!
          </h2>
        </Card>
        <Card className="col-span-1 row-span-2 flex flex-col shadow-xl">
          <CardHeader className="flex flex-col justify-start items-start">
            <CardTitle className="text-lg">Student Mark Distribution</CardTitle>
            <CardDescription className="font-light">No access.</CardDescription>
          </CardHeader>
          <div className="flex flex-col pl-7 pr-7 mb-7 h-full">
            <Bar data={data} options={options} />
          </div>
        </Card>
        <Card className="col-span-2 row-span-1 flex flex-col shadow-xl">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle className="text-lg">Class Overview</CardTitle>
          </CardHeader>
          <h2 className="px-6 font-normal text-sm">
            No roles assigned. To be able to see a class overview, please reach
            out to the administrator team.
          </h2>
        </Card>
      </div>
    </div>
  );
};

export default NoRoleView;
