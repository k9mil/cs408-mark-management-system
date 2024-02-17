import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "@/AuthProvider";

import Sidebar from "@/components/common/Sidebar";

import { studentService } from "@/services/StudentService";

import { IStudentBase } from "@/models/IStudent";
import { IUserDropdown } from "@/models/IUser";
import { IMarkRow } from "@/models/IMark";
import { IPersonalCircumstance } from "@/models/IPersonalCircumstance";

import StudentProfileDropdown from "./StudentProfileDropdown";
import { StudentProfileDataTable } from "./StudentProfileDataTable";

import { markService } from "@/services/MarkService";
import { personalCircumstanceService } from "@/services/PersonalCircumstanceService";

import { StudentColumns } from "../Students/StudentsColumns";

const StudentProfilePage = () => {
  const navigate = useNavigate();
  const { isLecturer, isAuthenticated, getAccessToken } = useAuth();

  const [students, setStudents] = useState<IStudentBase[]>([]);
  const [studentList, setStudentList] = React.useState<IUserDropdown[] | null>(
    null
  );

  const [studentOpen, setStudentOpen] = React.useState<boolean>(false);
  const [student, setStudent] = React.useState<string>("");
  const [studentMarks, setStudentMarks] = React.useState<IMarkRow[]>([]);
  const [studentPersonalCircumstances, setStudentPersonalCircumstances] =
    React.useState<IPersonalCircumstance[]>([]);

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

      const retrievePersonalCircumstances = async () => {
        try {
          if (accessToken) {
            const result =
              await personalCircumstanceService.getPersonalCircumstancesForStudent(
                student,
                accessToken
              );

            setStudentPersonalCircumstances(result);
          }
        } catch (error) {
          console.error(error);
        }
      };

      retrieveStudentMarks();
      retrievePersonalCircumstances();
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
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl overflow-hidden">
        <div className="m-8 flex flex-row space-x-12 w-full h-full">
          <div className="flex flex-col space-y-4 w-full h-full">
            <div className="flex 2xl:flex-col xl:flex-row 2xl:space-y-1 xl:space-x-2 2xl:space-x-0 xl:items-center 2xl:items-start">
              <h1 className="text-3xl font-bold">Student Profile</h1>
              <h2 className="text-gray-400">
                Enter a student name to view their history of uploaded marks
              </h2>
            </div>
            <div className="flex flex-row justify-between py-2 w-1/5">
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
            {student && student !== "" ? (
              <StudentProfileDataTable
                columns={StudentColumns}
                data={studentMarks}
                accessToken={accessToken}
              />
            ) : (
              <div className="flex flex-col justify-center items-center w-auto h-[70%] space-y-4">
                <div className="w-96 h-96">
                  <img src="/empty_state.svg" alt="No data found" />
                </div>
                <div className="space-y-2 flex flex-col justify-center items-center">
                  <h1 className="font-bold text-2xl">No data found</h1>
                  <h2 className="font-light text-md">
                    This area will fill with information once a user has been
                    picked.
                  </h2>
                </div>
              </div>
            )}
          </div>
          {student && student !== "" ? (
            <div className="flex flex-col">
              <h1 className="text-3xl font-bold mb-8">
                Personal Circumstances
              </h1>
              <div className="space-y-12">
                {studentPersonalCircumstances &&
                studentPersonalCircumstances.length > 0
                  ? studentPersonalCircumstances.map(
                      (personalCircumstance: IPersonalCircumstance) => (
                        <div className="flex flex-col">
                          <div className="space-x-2 flex flex-row">
                            <h2 className="font-sm font-bold">Details:</h2>
                            <h2 className="font-sm w-full">
                              {personalCircumstance.details}
                            </h2>
                          </div>
                          <div className="space-x-2 flex flex-row">
                            <h2 className="font-sm font-bold">Semester:</h2>
                            <h2 className="font-sm">
                              {personalCircumstance.semester}
                            </h2>
                          </div>
                          <div className="space-x-2 flex flex-row">
                            <h2 className="font-sm font-bold">Category:</h2>
                            <h2 className="font-sm">
                              {personalCircumstance.cat}
                            </h2>
                          </div>
                          <div className="space-x-2 flex flex-row">
                            <h2 className="font-sm font-bold">Comments:</h2>
                            <h2 className="font-sm">
                              {personalCircumstance.comments}
                            </h2>
                          </div>
                        </div>
                      )
                    )
                  : null}
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default StudentProfilePage;
