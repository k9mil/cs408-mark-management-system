import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { Button } from "@/components/common/Button";

import { useAuth } from "@/AuthProvider";

import Sidebar from "@/components/common/Sidebar";

import { studentService } from "@/services/StudentService";

import { IStudentBase } from "@/models/IStudent";
import { IUserDropdown } from "@/models/IUser";

import StudentProfileDropdown from "./StudentProfileDropdown";
import { StudentProfileDataTable } from "./StudentProfileDataTable";

import { markService } from "@/services/MarkService";

import { StudentColumns } from "../Students/StudentsColumns";

const StudentProfilePage = () => {
  const navigate = useNavigate();
  const { isLecturer, isAuthenticated, getAccessToken } = useAuth();

  const [students, setStudents] = useState<IStudentBase[]>([]);
  const [studentList, setStudentList] = React.useState<IUserDropdown[] | null>(
    null
  );

  const [searchValue, setSearchValue] = useState<string | null>(null);
  const [studentOpen, setStudentOpen] = React.useState<boolean>(false);
  const [student, setStudent] = React.useState<string>("");
  const [studentMarks, setStudentMarks] = React.useState<string>("");

  const accessToken = getAccessToken();

  useEffect(() => {
    document.title = "Mark Management System | Student Profile";

    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  const studentsData = async () => {
    try {
      if (accessToken) {
        if (isLecturer) {
          const result = await studentService.getStudents(accessToken);
          setStudents(result);
          console.log(result);
        }
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    studentsData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (student !== "") {
      const retrieveStudentMarks = async () => {
        try {
          if (accessToken) {
            const result = await markService.getMarksForStudent(
              student,
              accessToken
            );

            setStudentMarks(result);
          }
        } catch (error) {
          console.error(error);
        }
      };

      retrieveStudentMarks();
    }
  }, [student, accessToken]);

  useEffect(() => {
    if (students && Array.isArray(students)) {
      const mappedStudents = students.map((user: IStudentBase) => ({
        value: user.reg_no,
        label: user.student_name,
      }));

      setStudentList(mappedStudents);
    }
  }, [students]);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl">
        <div className="m-8 flex flex-col space-y-4">
          <div className="flex 2xl:flex-col xl:flex-row 2xl:space-y-1 xl:space-x-2 2xl:space-x-0 xl:items-center 2xl:items-start">
            <h1 className="text-3xl font-bold">Student Profile</h1>
            <h2 className="text-gray-400">
              Enter a student name to view their history of uploaded marks
            </h2>
          </div>
          <div className="flex flex-row justify-between py-2">
            <div className="flex items-center w-1/5">
              {studentList !== null && studentList.length !== 0 ? (
                <StudentProfileDropdown
                  student={student}
                  studentOpen={studentOpen}
                  setStudent={setStudent}
                  setStudentOpen={setStudentOpen}
                  studentList={studentList}
                />
              ) : null}
            </div>
          </div>
          {student && student !== "" ? (
            <StudentProfileDataTable
              columns={StudentColumns}
              data={studentMarks}
              accessToken={accessToken}
            />
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default StudentProfilePage;
