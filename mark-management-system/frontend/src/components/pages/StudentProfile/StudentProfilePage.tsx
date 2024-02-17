import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "@/AuthProvider";

import Sidebar from "@/components/common/Sidebar";

import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/components/common/Card";

import { studentService } from "@/services/StudentService";

import { IStudentBase } from "@/models/IStudent";
import { IUserDropdown } from "@/models/IUser";
import { IMarkRow } from "@/models/IMark";
import { IPersonalCircumstance } from "@/models/IPersonalCircumstance";

import StudentProfileDropdown from "./StudentProfileDropdown";
import { StudentProfileDataTable } from "./StudentProfileDataTable";

import { markService } from "@/services/MarkService";
import { personalCircumstanceService } from "@/services/PersonalCircumstanceService";

import { StudentProfileColumns } from "../Students/StudentsColumns";

import { ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/24/outline";

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

  const [currentPersonalCircumstance, setCurrentPersonalCircumstance] =
    useState<number>(0);

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
            console.log(result);
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

  const handlePrev = () => {
    if (currentPersonalCircumstance > 0) {
      setCurrentPersonalCircumstance(currentPersonalCircumstance - 1);
    }
  };

  const handleNext = () => {
    if (currentPersonalCircumstance < studentPersonalCircumstances.length - 1) {
      setCurrentPersonalCircumstance(currentPersonalCircumstance + 1);
    }
  };

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl">
        <div className="mt-8 ml-8 mr-8 flex flex-col space-y-4">
          <div className="flex 2xl:flex-col xl:flex-row 2xl:space-y-1 xl:space-x-2 2xl:space-x-0 xl:items-center 2xl:items-start">
            <h1 className="text-3xl font-bold">Student Profile</h1>
            <h2 className="text-gray-400">
              Enter a student name to view their history of uploaded marks
            </h2>
          </div>
        </div>
        <div className="flex flex-row w-full h-[80vh]">
          <div
            className={`flex flex-col space-y-1 m-8 ${
              student && student !== "" ? "w-1/2" : "w-full"
            }`}
          >
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
                columns={StudentProfileColumns}
                data={studentMarks}
                accessToken={accessToken}
              />
            ) : (
              <div className="flex flex-col justify-center items-center m-auto h-full space-y-4">
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
            <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
          ) : null}
          {student &&
          student !== "" &&
          studentMarks &&
          studentMarks.length > 0 &&
          studentPersonalCircumstances &&
          studentPersonalCircumstances.length > 0 ? (
            <div className="flex flex-col justify-center items-center w-2/5 m-auto space-y-8">
              <Card className="w-full h-1/2 space-y-2 flex items-center justify-center flex-col shadow-xl p-8">
                <CardHeader className="flex flex-row justify-between items-center p-0">
                  <CardTitle className="text-2xl font-bold mb-6">
                    Student Details
                  </CardTitle>
                </CardHeader>
                <div className="flex flex-row w-full justify-between items-center">
                  <div className="flex flex-col space-y-6 w-2/3">
                    <div className="flex flex-col space-y-2">
                      <div className="flex flex-row space-x-2 w-full">
                        <h2 className="text-md font-semibold">Name:</h2>
                        <h2 className="text-sm font-regular flex justify-self-center self-center">
                          {studentMarks[0].student_name}
                        </h2>
                      </div>
                      <div className="flex flex-row space-x-2 w-full">
                        <h2 className="text-md font-semibold">
                          Registration Number:
                        </h2>
                        <h2 className="text-sm font-regular flex justify-self-center self-center">
                          {studentMarks[0].reg_no}
                        </h2>
                      </div>
                      <div className="flex flex-row space-x-2 w-full">
                        <h2 className="text-md font-semibold">Degree Name:</h2>
                        <h2 className="text-sm font-regular flex justify-self-center self-center">
                          {studentMarks[0].degree_name}
                        </h2>
                      </div>
                      <div className="flex flex-row space-x-2 w-full">
                        <h2 className="text-md font-semibold">Degree Level:</h2>
                        <h2 className="text-sm font-regular flex justify-self-center self-center">
                          {studentMarks[0].degree_level}
                        </h2>
                      </div>
                    </div>
                  </div>
                  <div className="flex flex-col space-y-6 w-1/3">
                    <CardContent className="flex flex-row justify-around p-0">
                      <div className="flex flex-col justify-center items-center">
                        <h1 className="font-bold text-3xl text-primary-blue">
                          10%
                        </h1>
                        <h1 className="text-xs">Pass Rate</h1>
                      </div>
                      <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                      <div className="flex flex-col justify-center items-center">
                        <h1 className="font-bold text-3xl text-primary-blue">
                          10%
                        </h1>
                        <h1 className="text-xs">Mean</h1>
                      </div>
                    </CardContent>
                    <CardContent className="flex flex-row justify-around p-0">
                      <div className="flex flex-col justify-center items-center">
                        <h1 className="font-bold text-3xl text-primary-blue">
                          10%
                        </h1>
                        <h1 className="text-xs">Median</h1>
                      </div>
                      <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                      <div className="flex flex-col justify-center items-center">
                        <h1 className="font-bold text-3xl text-primary-blue">
                          10%
                        </h1>
                        <h1 className="text-xs">Mode</h1>
                      </div>
                    </CardContent>
                  </div>
                </div>
              </Card>
              <Card className="w-full h-1/2 space-y-2 flex items-center justify-center flex-col shadow-xl p-8">
                <CardHeader className="flex flex-row justify-between items-center p-0">
                  <CardTitle className="text-2xl font-bold mb-6">
                    Personal Circumstances
                  </CardTitle>
                </CardHeader>
                <div className="flex flex-row w-full justify-between items-center">
                  <div className="flex flex-col space-y-6 w-full">
                    <div className="flex flex-col space-y-2">
                      <div className="flex flex-row space-x-2 w-full">
                        <h2 className="text-md font-semibold">Details:</h2>
                        <h2 className="text-sm font-regular flex justify-self-center self-center">
                          {
                            studentPersonalCircumstances[
                              currentPersonalCircumstance
                            ].details
                          }
                        </h2>
                      </div>
                      <div className="flex flex-row space-x-2 w-full">
                        <h2 className="text-md font-semibold">Semester:</h2>
                        <h2 className="text-sm font-regular flex justify-self-center self-center">
                          {
                            studentPersonalCircumstances[
                              currentPersonalCircumstance
                            ].semester
                          }
                        </h2>
                      </div>
                      <div className="flex flex-row space-x-2 w-full">
                        <h2 className="text-md font-semibold">Category:</h2>
                        <h2 className="text-sm font-regular flex justify-self-center self-center">
                          {
                            studentPersonalCircumstances[
                              currentPersonalCircumstance
                            ].cat
                          }
                        </h2>
                      </div>
                      <div className="flex flex-row space-x-2 w-full">
                        <h2 className="text-md font-semibold">Comments:</h2>
                        <h2 className="text-sm font-regular flex justify-self-center self-center">
                          {
                            studentPersonalCircumstances[
                              currentPersonalCircumstance
                            ].comments
                          }
                        </h2>
                      </div>
                    </div>
                    <div className="flex justify-end items-end w-full">
                      <ChevronLeftIcon
                        className="h-6 w-6 text-black hover:cursor-pointer"
                        onClick={handlePrev}
                      />
                      <ChevronRightIcon
                        className="h-6 w-6 text-black hover:cursor-pointer"
                        onClick={handleNext}
                      />
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default StudentProfilePage;
