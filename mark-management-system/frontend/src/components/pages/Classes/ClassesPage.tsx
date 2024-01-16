import React, { useEffect, useState } from "react";

import Sidebar from "../../common/Sidebar";

import { ClassesDataTable } from "./ClassesDataTable";
import { Class, ClassColumns } from "./ClassesColumns";
import { classService } from "../../../services/ClassService";

const ClassesPage = () => {
  const [classes, setClasses] = useState<Class[]>([]);

  useEffect(() => {
    const classData = async () => {
      try {
        const result = await classService.getClasses();
        setClasses(result);
      } catch (error) {
        console.error(error);
      }
    };

    classData();
  }, []);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl">
        <div className="m-8 flex flex-col space-y-4">
          <div className="flex flex-col space-y-4">
            <h1 className="text-3xl font-bold">Classes</h1>
            <h2 className="text-gray-400">
              View a list of classes in the system
            </h2>
          </div>
          <ClassesDataTable columns={ClassColumns} data={classes} />
        </div>
      </div>
    </div>
  );
};

export default ClassesPage;
