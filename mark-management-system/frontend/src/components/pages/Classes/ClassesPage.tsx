import * as React from "react";

import Sidebar from "../../common/Sidebar";

import { ClassesDataTable } from "./ClassesDataTable";
import { Class, User, ClassColumns } from "./ClassesColumns";

const classLecturer: User = {
  first_name: "Joe",
  last_name: "Doe",
};

const classData: Class[] = [
  {
    name: "A class",
    code: "CS426",
    credit: 10,
    credit_level: 4,
    number_of_students: 52,
    lecturer: classLecturer,
  },
  {
    name: "A class",
    code: "CS426",
    credit: 10,
    credit_level: 4,
    number_of_students: 52,
    lecturer: classLecturer,
  },
];

const ClassesPage = () => {
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
          <ClassesDataTable columns={ClassColumns} data={classData} />
        </div>
      </div>
    </div>
  );
};

export default ClassesPage;
