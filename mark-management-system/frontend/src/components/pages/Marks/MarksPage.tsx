import React, { useState, useEffect, useRef } from "react";

import Papa from "papaparse";

import { useNavigate } from "react-router-dom";

import { useAuth } from "@/AuthProvider";

import { Button } from "@/components/common/Button";

import Sidebar from "@/components/common/Sidebar";

import MarksInfoBox from "./MarksInfoBox";
import MarksUploadedFile from "./MarksUploadedFile";

import { IMark, IMarkRow } from "@/models/IMark";
import { IStudentCreate } from "@/models/IStudent";

import { classService } from "@/services/ClassService";
import { studentService } from "@/services/StudentService";
import { markService } from "@/services/MarkService";
import { degreeService } from "@/services/DegreeService";

import { toast } from "sonner";

import { DocumentArrowUpIcon } from "@heroicons/react/24/outline";

import { Card, CardHeader, CardTitle } from "@/components/common/Card";
import { validateParsedFile } from "@/utils/FileUploadUtils";
import { toLowerCase } from "@/utils/Utils";

const MarksPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, getAccessToken } = useAuth();

  useEffect(() => {
    document.title = "Mark Management System | Marks";

    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  const filePickedLocal = useRef<HTMLInputElement>(null);

  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const accessToken = getAccessToken();

  const uploadMarks = async () => {
    const uniqueDegrees: Set<string> = new Set();

    try {
      if (!accessToken) {
        toast.error("Access token is missing.");

        return;
      }

      const parsedFile = await parseFileContents();
      let parsedFileToLower;

      if (parsedFile) {
        parsedFileToLower = toLowerCase(parsedFile);
      }

      if (parsedFileToLower && validateParsedFile(parsedFileToLower.slice(0))) {
        parsedFileToLower.forEach((row) => {
          uniqueDegrees.add(row.degree_name);
        });

        const degreesExist = await checkDegreesExist(uniqueDegrees);
        const classExist = await checkClassExists(
          parsedFileToLower.slice(0)[0].class_code
        );

        if (degreesExist && classExist) {
          for (const [index, row] of parsedFileToLower.slice(0).entries()) {
            await checkStudentExists(
              row.reg_no,
              row.student_name,
              row.degree_name,
              index
            );

            await checkMarkExists(
              row.mark,
              row.unique_code,
              row.class_code,
              row.reg_no,
              index
            );
          }

          toast.success("Your file has been succesfully uploaded!");
        }
      }
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when uploading the marks.");
    }
  };

  const parseFileContents = async (): Promise<IMarkRow[] | null> => {
    if (file) {
      return new Promise((resolve, reject) => {
        Papa.parse(file, {
          complete: (results) => {
            resolve(results.data as IMarkRow[]);
          },
          header: true,
          error: (error) => {
            reject(error);
          },
        });
      });
    }

    return null;
  };

  const checkDegreesExist = async (
    uniqueDegrees: Set<string>
  ): Promise<boolean> => {
    try {
      if (accessToken) {
        const degreeDetails = await degreeService.getDegrees(
          uniqueDegrees,
          accessToken
        );

        if (degreeDetails.statusCode !== 200) {
          toast.error(
            `Something went wrong when uploading the marks. ${degreeDetails.data}.`
          );

          return false;
        }

        return true;
      }

      return false;
    } catch (error) {
      console.error(error);
      toast.error(`Something went wrong when uploading the marks.`);

      return false;
    }
  };

  const checkClassExists = async (classCode: string): Promise<boolean> => {
    try {
      if (accessToken) {
        const classDetails = await classService.getClass(
          classCode,
          accessToken
        );

        if (classDetails.statusCode !== 200) {
          toast.error(
            `Something went wrong when uploading the marks. ${classDetails.data}.`
          );

          return false;
        }

        return true;
      }

      return false;
    } catch (error) {
      console.error(error);
      toast.error(`Something went wrong when uploading the marks.`);

      return false;
    }
  };

  const checkStudentExists = async (
    studentRegNo: string,
    studentName: string,
    degreeName: string,
    index: number
  ) => {
    try {
      if (accessToken) {
        const studentDetails = await studentService.getStudent(
          studentRegNo,
          accessToken
        );

        if (studentDetails.statusCode !== 200) {
          if (studentDetails.statusCode === 404) {
            const degreeId = await getDegreeDetails(degreeName, index);

            if (degreeId) {
              await createStudent(studentRegNo, studentName, degreeId, index);
            }
          } else {
            toast.error(
              `Something went wrong when checking if the student exists. ${studentDetails.data}.`
            );
          }
        }
      }
    } catch (error) {
      console.error(error);

      toast.error(
        `Something went wrong when uploading the marks for Row ${index + 2}.`
      );
    }
  };

  const checkMarkExists = async (
    mark: number,
    markUniqueCode: string,
    classCode: string,
    regNo: string,
    index: number
  ) => {
    try {
      if (accessToken) {
        const markDetails = await markService.getMark(
          markUniqueCode,
          accessToken
        );

        if (markDetails.statusCode !== 200) {
          if (markDetails.statusCode === 404) {
            const classId = await getClassDetails(classCode, index);
            const studentId = await getStudentDetails(regNo, index);

            if (classId && studentId) {
              await createMark(mark, markUniqueCode, studentId, classId, index);
            }
          } else {
            toast.error(
              `Something went wrong when uploading the marks for Row ${
                index + 2
              }. ${markDetails.data}.`
            );
          }
        } else {
          toast.error(
            `Something went wrong when uploading the marks for Row ${
              index + 2
            }. The mark has already been uploaded.`
          );
        }
      }
    } catch (error) {
      console.error(error);

      toast.error(
        `Something went wrong when uploading the marks for Row ${index + 2}.`
      );
    }
  };

  const createStudent = async (
    studentRegNo: string,
    studentName: string,
    degreeId: number,
    index: number
  ) => {
    // NOTE: THIS IS ONLY FOR TESTING/DEVELOPMENT PURPOSES. TO BE DELETED BEFORE FINAL PRODUCT.
    try {
      if (accessToken) {
        const studentDetails = {
          reg_no: studentRegNo,
          student_name: studentName,
          personal_circumstances: null,
          degree_id: degreeId,
        };

        const studentCreated = await studentService.createStudent(
          studentDetails,
          accessToken
        );

        if (studentCreated.statusCode !== 200) {
          toast.error(
            `Something went wrong when uploading the marks for Row ${
              index + 2
            }. ${studentCreated.data}`
          );
        } else {
          toast.success("Student was created successfully! DEV.");
        }
      }
    } catch (error) {
      console.error(error);

      toast.error(
        `Something went wrong when creating a student for Row ${
          index + 2
        }. DEV.`
      );
    }
  };

  const createMark = async (
    mark: number,
    markUniqueCode: string,
    studentId: number,
    classId: number,
    index: number
  ) => {
    try {
      if (accessToken) {
        const markDetails: IMark = {
          unique_code: markUniqueCode,
          mark: mark,
          class_id: classId,
          student_id: studentId,
        };

        const markCreated = await markService.createMark(
          markDetails,
          accessToken
        );

        if (markCreated.statusCode !== 200) {
          toast.error(
            `Something went wrong when uploading the marks for Row ${
              index + 2
            }. ${markCreated.data}`
          );
        } else {
          toast.success("Mark was uploaded!");
        }
      }
    } catch (error) {
      console.error(error);

      toast.error(
        `Something went wrong when uploading a mark for Row ${index + 2}.`
      );
    }
  };

  const getDegreeDetails = async (degreeName: string, index: number) => {
    try {
      if (accessToken) {
        const degreeDetails = await degreeService.getDegree(
          degreeName,
          accessToken
        );

        return degreeDetails.data.id;
      }
    } catch (error) {
      console.error(error);

      toast.error(
        `Something went wrong when uploading the marks for Row ${index + 2}.`
      );
    }
  };

  const getStudentDetails = async (studentRegNo: string, index: number) => {
    try {
      if (accessToken) {
        const studentDetails = await studentService.getStudent(
          studentRegNo,
          accessToken
        );

        return studentDetails.data.id;
      }
    } catch (error) {
      console.error(error);

      toast.error(
        `Something went wrong when uploading the marks for Row ${index + 2}.`
      );
    }
  };

  const getClassDetails = async (classCode: string, index: number) => {
    try {
      if (accessToken) {
        const classDetails = await classService.getClass(
          classCode,
          accessToken
        );

        return classDetails.data.id;
      }
    } catch (error) {
      console.error(error);

      toast.error(
        `Something went wrong when uploading the marks for Row ${index + 2}.`
      );
    }
  };

  const preventEventDefaults = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    preventEventDefaults(e);
    setIsDragging(true);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    preventEventDefaults(e);
    setIsDragging(false);

    if (
      e.dataTransfer.files &&
      validateFileSizeAndExtension(e.dataTransfer.files[0])
    ) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    preventEventDefaults(e);
    setIsDragging(false);
  };

  const handleFileLocal = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    e.stopPropagation();

    if (e.target.files && validateFileSizeAndExtension(e.target.files[0])) {
      setFile(e.target.files[0]);
      e.target.value = "";
    }
  };

  const handleClick = () => {
    if (filePickedLocal && filePickedLocal.current !== null) {
      filePickedLocal.current.click();
    }
  };

  const validateFileSizeAndExtension = (file: File): boolean => {
    if (file.size > 5242880) {
      toast.error("The file size should not exceeed 5MB.");

      return false;
    }

    if (file.type !== "text/csv") {
      toast.error("The file should be in a CSV format.");
      return false;
    }

    return true;
  };

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center">
        <Card className="w-1/2 h-3/5 space-y-4 p-6 flex flex-col justify-between">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle>Upload Marks</CardTitle>
          </CardHeader>
          <div
            className={
              isDragging
                ? "border-primary-blue bg-slate-50 mx-6 rounded-md border-2 border-dashed flex flex-col justify-center items-center space-y-8 h-3/4"
                : file
                ? "border-primary-blue bg-gray-100 mx-6 rounded-md border-2 flex flex-col justify-center items-center space-y-8 h-3/4 opacity-50"
                : "mx-6 rounded-md border-2 border-dashed border-gray-300 flex flex-col justify-center items-center space-y-8 h-3/4"
            }
            onDragOver={file === null ? handleDragOver : undefined}
            onDragLeave={file === null ? handleDragLeave : undefined}
            onDrop={file === null ? handleDrop : undefined}
          >
            <DocumentArrowUpIcon className="h-12 w-12 text-card-foreground" />
            <h2 className="text-card-foreground font-semibold">
              Drag and Drop a file here or{" "}
              <span
                onClick={file === null ? handleClick : undefined}
                className={
                  file
                    ? "underline font-bold underline-offset-4"
                    : "underline font-bold underline-offset-4 cursor-pointer"
                }
              >
                Choose File
                <input
                  className="hidden"
                  type="file"
                  ref={filePickedLocal}
                  onChange={handleFileLocal}
                ></input>
              </span>
            </h2>
          </div>
          {file ? <MarksUploadedFile file={file} setFile={setFile} /> : null}
          <div className="h-1/4 flex flex-col justify-end space-y-4">
            <div className="flex flex-row justify-between mx-6">
              <h2 className="text-sm text-gray-400">Supported formats: CSV</h2>
              <h2 className="text-sm text-gray-400">Maximum size: 5MB</h2>
            </div>
            <div className="flex flex-row mx-6 justify-between items-center">
              <MarksInfoBox />
              <div className="flex flex-row space-x-4">
                <Button variant="secondary" className="w-20">
                  Cancel
                </Button>
                <Button
                  disabled={!file}
                  className="w-20"
                  onClick={() => {
                    uploadMarks();
                    setFile(null);
                  }}
                >
                  Next
                </Button>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default MarksPage;
