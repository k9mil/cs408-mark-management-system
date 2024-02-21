import React, { useEffect, useState } from "react";

import { useNavigate, Link } from "react-router-dom";

import { useAuth } from "@/AuthProvider";

import Sidebar from "@/components/common/Sidebar";

import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/components/common/Card";

import { studentService } from "@/services/StudentService";

import {
  IStudent,
  IStudentBase,
  IStudentDetailsWithStatistics,
} from "@/models/IStudent";
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
  const { isLecturer, isAdmin, isAuthenticated, getAccessToken } = useAuth();

  const [students, setStudents] = useState<IStudentBase[]>([]);
  const [studentList, setStudentList] = React.useState<IUserDropdown[] | null>(
    null
  );

  const [studentOpen, setStudentOpen] = React.useState<boolean>(false);
  const [student, setStudent] = React.useState<string>("");
  const [studentStatistics, setStudentStatistics] =
    React.useState<IStudentDetailsWithStatistics>();
  const [studentMarks, setStudentMarks] = React.useState<IMarkRow[]>([]);
  const [studentData, setStudentData] = React.useState<IStudent>();
  const [studentPersonalCircumstances, setStudentPersonalCircumstances] =
    React.useState<IPersonalCircumstance[]>([]);
  const [isUpdated, setIsUpdated] = useState(false);

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
        if (isLecturer || isAdmin) {
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

      const retrieveStudentsStatistics = async () => {
        try {
          if (accessToken) {
            const result = await studentService.getStudentStatistics(
              student,
              accessToken
            );

            setStudentStatistics(result);
          }
        } catch (error) {
          console.error(error);
        }
      };

      const retrieveStudentData = async () => {
        try {
          if (accessToken) {
            const result = await studentService.getStudent(
              student,
              accessToken
            );

            if (result.statusCode === 200) {
              setStudentData(result.data);
            }
          }
        } catch (error) {
          console.error(error);
        }
      };

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

      retrievePersonalCircumstances();
      retrieveStudentsStatistics();
      retrieveStudentData();
      retrieveStudentMarks();

      setCurrentPersonalCircumstance(0);
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

  useEffect(() => {
    if (studentData && studentData.classes.length > 0) {
      const updatedMarks = studentMarks.map((mark) => {
        const matchClassWithCode = studentData.classes.find(
          (class_) => class_.code === mark.class_code
        );

        if (matchClassWithCode) {
          return {
            ...mark,
            academic_misconduct: matchClassWithCode.academic_misconduct,
          };
        }

        return mark;
      });

      setStudentMarks(updatedMarks);
      setIsUpdated(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [studentData]);

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
            {student && student !== "" && studentData && isUpdated ? (
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
          {student && student !== "" ? (
            <div className="flex flex-col justify-center items-center w-2/5 m-auto space-y-8">
              <Card className="w-full h-1/2 space-y-2 flex items-center justify-center flex-col shadow-xl p-8">
                <CardHeader className="flex flex-row justify-between items-center p-0">
                  <CardTitle className="2xl:text-2xl xl:text-xl font-bold mb-6">
                    Student Details
                  </CardTitle>
                </CardHeader>
                {studentData || studentStatistics ? (
                  <div className="flex flex-row w-full justify-between items-center">
                    {studentData ? (
                      <div className="flex flex-col space-y-6 w-2/3">
                        <div className="flex flex-col space-y-2">
                          <div className="flex flex-row space-x-2 w-full">
                            <h2 className="2xl:text-base xl:text-sm font-semibold">
                              Name:
                            </h2>
                            <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                              {studentData.student_name}
                            </h2>
                          </div>
                          <div className="flex flex-row space-x-2 w-full">
                            <h2 className="2xl:text-base xl:text-sm font-semibold">
                              Registration Number:
                            </h2>
                            <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                              {studentData.reg_no}
                            </h2>
                          </div>
                          <div className="flex flex-row space-x-2 2xl:w-full">
                            <h2 className="2xl:text-base xl:text-sm font-semibold">
                              Degree Name:
                            </h2>
                            <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                              {studentData.degree.name}
                            </h2>
                          </div>
                          <div className="flex flex-row space-x-2 w-full">
                            <h2 className="2xl:text-base xl:text-sm font-semibold">
                              Degree Level:
                            </h2>
                            <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                              {studentData.degree.level}
                            </h2>
                          </div>
                        </div>
                      </div>
                    ) : null}
                    {studentStatistics ? (
                      <div className="flex flex-col space-y-8 w-1/3">
                        <CardContent className="flex flex-row space-x-4 justify-around p-0">
                          <div className="flex flex-col justify-center items-center">
                            <h1 className="font-bold 2xl:text-3xl xl:text-xl text-primary-blue">
                              {studentStatistics.pass_rate === -1
                                ? "N/A"
                                : `${studentStatistics.pass_rate}%`}
                            </h1>
                            <h1 className="text-xs hidden xl:inline 2xl:hidden">
                              Pass R.
                            </h1>
                            <h1 className="text-xs hidden 2xl:inline">
                              Pass Rate
                            </h1>
                          </div>
                          <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                          <div className="flex flex-col justify-center items-center">
                            <h1 className="font-bold 2xl:text-3xl xl:text-xl text-primary-blue">
                              {studentStatistics.mean === -1
                                ? "N/A"
                                : `${studentStatistics.mean}%`}
                            </h1>
                            <h1 className="text-xs">Mean</h1>
                          </div>
                        </CardContent>
                        <CardContent className="space-x-4 flex flex-row justify-around p-0">
                          <div className="flex flex-col justify-center items-center">
                            <h1 className="font-bold 2xl:text-3xl xl:text-xl text-primary-blue">
                              {studentStatistics.median === -1
                                ? "N/A"
                                : `${studentStatistics.median}%`}
                            </h1>
                            <h1 className="text-xs">Median</h1>
                          </div>
                          <div className="border-r-[1px] border-l-[1px] border-gray-200"></div>
                          <div className="flex flex-col justify-center items-center">
                            <h1 className="font-bold 2xl:text-3xl xl:text-xl text-primary-blue">
                              {studentStatistics.mode === -1
                                ? "N/A"
                                : `${studentStatistics.mode}%`}
                            </h1>
                            <h1 className="text-xs">Mode</h1>
                          </div>
                        </CardContent>
                      </div>
                    ) : null}
                  </div>
                ) : (
                  <h2 className="text-base font-regular">
                    It seems like there are no student details available at the
                    moment. If you are expecting to see something here,{" "}
                    <Link
                      to="/help"
                      className="text-blue-400 font-bold hover:underline"
                    >
                      contact an administrator
                    </Link>
                    .
                  </h2>
                )}
              </Card>
              <Card className="w-full h-1/2 space-y-2 flex items-center justify-center flex-col shadow-xl p-8">
                <CardHeader className="flex flex-row justify-between items-center p-0">
                  <CardTitle className="text-2xl font-bold mb-6">
                    Personal Circumstances
                  </CardTitle>
                </CardHeader>
                {studentPersonalCircumstances &&
                studentPersonalCircumstances.length > 0 ? (
                  <div className="flex flex-row w-full justify-between items-center">
                    <div className="flex flex-col space-y-6 w-full">
                      <div className="flex flex-col space-y-2">
                        <div className="flex flex-row space-x-2 w-full">
                          <h2 className="2xl:text-base xl:text-sm font-semibold">
                            Details:
                          </h2>
                          <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                            {
                              studentPersonalCircumstances[
                                currentPersonalCircumstance
                              ].details
                            }
                          </h2>
                        </div>
                        <div className="flex flex-row space-x-2 w-full">
                          <h2 className="2xl:text-base xl:text-sm font-semibold">
                            Semester:
                          </h2>
                          <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                            {
                              studentPersonalCircumstances[
                                currentPersonalCircumstance
                              ].semester
                            }
                          </h2>
                        </div>
                        <div className="flex flex-row space-x-2 w-full">
                          <h2 className="2xl:text-base xl:text-sm font-semibold">
                            Category:
                          </h2>
                          <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
                            {
                              studentPersonalCircumstances[
                                currentPersonalCircumstance
                              ].cat
                            }
                          </h2>
                        </div>
                        <div className="flex flex-row space-x-2 w-full">
                          <h2 className="2xl:text-base xl:text-sm font-semibold">
                            Comments:
                          </h2>
                          <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-center self-center">
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
                          className={`h-6 w-6 ${
                            currentPersonalCircumstance === 0
                              ? "text-gray-400"
                              : "hover:cursor-pointer text-black"
                          }`}
                          onClick={handlePrev}
                        />
                        <ChevronRightIcon
                          className={`h-6 w-6 ${
                            currentPersonalCircumstance ===
                            studentPersonalCircumstances.length - 1
                              ? "text-gray-400"
                              : "hover:cursor-pointer text-black"
                          }`}
                          onClick={handleNext}
                        />
                      </div>
                    </div>
                  </div>
                ) : (
                  <h2 className="text-base font-regular">
                    It seems like there are no recorded personal circumstances
                    for this student. If you are expecting to see something
                    here,{" "}
                    <Link
                      to="/help"
                      className="text-blue-400 font-bold hover:underline"
                    >
                      contact an administrator
                    </Link>
                    .
                  </h2>
                )}
              </Card>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default StudentProfilePage;
