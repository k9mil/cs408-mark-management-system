import React, { useEffect } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import Sidebar from "../../common/Sidebar";
import { StudentsDataTable } from "./StudentsDataTable";
import { Student, StudentColumns } from "./StudentsColumns";

const studentData: Student[] = [
  {
    class_code: "CS408",
    registration_number: "hea92741",
    mark: 70,
    student_name: "Joanna Thompson",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "szi88904",
    mark: 64,
    student_name: "Bryan Lopez",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "hea92741",
    mark: 70,
    student_name: "Joanna Thompson",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "szi88904",
    mark: 64,
    student_name: "Bryan Lopez",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "hea92741",
    mark: 70,
    student_name: "Joanna Thompson",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "szi88904",
    mark: 64,
    student_name: "Bryan Lopez",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "hea92741",
    mark: 70,
    student_name: "Joanna Thompson",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "szi88904",
    mark: 64,
    student_name: "Bryan Lopez",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "hea92741",
    mark: 70,
    student_name: "Joanna Thompson",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "szi88904",
    mark: 64,
    student_name: "Bryan Lopez",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "hea92741",
    mark: 70,
    student_name: "Joanna Thompson",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "szi88904",
    mark: 64,
    student_name: "Bryan Lopez",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "szi88904",
    mark: 64,
    student_name: "Bryan Lopez",
    degree_level: "BSc",
    degree: "Computer Science",
  },
  {
    class_code: "CS408",
    registration_number: "szi88904",
    mark: 64,
    student_name: "Bryan Lopez",
    degree_level: "BSc",
    degree: "Computer Science",
  },
];

const StudentsPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl">
        <div className="m-8 flex flex-col space-y-4">
          <div className="flex flex-col space-y-4">
            <h1 className="text-3xl font-bold">Students</h1>
            <h2 className="text-gray-400">
              View the students that you have uploaded marks for
            </h2>
          </div>
          <StudentsDataTable columns={StudentColumns} data={studentData} />
        </div>
      </div>
    </div>
  );
};

export default StudentsPage;
