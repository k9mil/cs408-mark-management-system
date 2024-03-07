import React, { useEffect, useState, useRef } from "react";

import Papa from "papaparse";

import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../AuthProvider";

import { Button } from "@/components/common/Button";
import { Card, CardHeader, CardTitle } from "@/components/common/Card";

import Sidebar from "@/components/common/Sidebar";

import { toast } from "sonner";

import { DocumentArrowUpIcon } from "@heroicons/react/24/outline";

import MarksUploadedFile from "../Upload/MarksUploadedFile";
import ConvertSelectionCombobox from "./ConvertSelectionCombobox";

import { IMarkMMS, IMarkMyPlace, IMarkPegasus, IMarkRow } from "@/models/IMark";
import { IStudent } from "@/models/IStudent";

import {
  exportToCSV,
  toLowerCaseIMarkMyPlace,
  toLowerCaseIMarkRow,
} from "@/utils/Utils";

import {
  validateFileSizeAndExtension,
  validateMyPlaceFile,
  validateUploadFile,
} from "@/utils/FileUploadUtils";

import { studentService } from "@/services/StudentService";

import ConvertInfoBox from "./ConvertInfoBox";
import { classService } from "@/services/ClassService";
import { IClass } from "@/models/IClass";

const ConvertPage = () => {
  const navigate = useNavigate();
  const { isAdmin, isLecturer, isAuthenticated, getAccessToken } = useAuth();

  useEffect(() => {
    document.title = "Mark Management System | Convert";

    if (!isAuthenticated || (!isAdmin && !isLecturer)) {
      navigate("/");
    }
  }, [navigate, isAuthenticated, isAdmin, isLecturer]);

  const [conversionOpen, setConversionOpen] = React.useState<boolean>(false);
  const [conversionType, setConversionType] = React.useState<string>("");

  const filePickedLocal = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const accessToken = getAccessToken();

  const processFile = async () => {
    try {
      if (!accessToken) {
        toast.error("Access token is missing.");

        return;
      }

      if (conversionType === "myplace_to_mms") {
        const parsedFile = await parseMyPlaceFile();
        const convertedObjects = [];

        let parsedFileToLower;
        let convertedObject;

        if (parsedFile) {
          parsedFileToLower = toLowerCaseIMarkMyPlace(parsedFile);
        }

        const fileContents = parsedFileToLower
          ?.slice(0)
          .filter(
            (fileContent) =>
              !Object.values(fileContent).every((value) => value === "")
          );

        if (fileContents && validateMyPlaceFile(fileContents)) {
          for (const [index, row] of fileContents.entries()) {
            const studentDetails = await retrieveStudentDetails(
              row.reg_no,
              index
            );

            if (studentDetails) {
              convertedObject = convertToMMS(row, studentDetails);
              convertedObjects.push(convertedObject);
            }
          }

          exportToCSV(
            convertedObjects,
            "The converted file has been downloaded.",
            "converted_to_mms_format"
          );

          toast.success("Your file has been succesfully converted!");
        }
      }

      if (conversionType === "mms_to_pegasus") {
        const parsedFile = await parseMarksManagementSystemFile();
        const convertedObjects = [];

        let parsedFileToLower;
        let convertedObject;

        if (parsedFile) {
          parsedFileToLower = toLowerCaseIMarkRow(parsedFile);
        }

        const fileContents = parsedFileToLower
          ?.slice(0)
          .filter(
            (fileContent) =>
              !Object.values(fileContent).every((value) => value === "")
          );

        if (fileContents && validateUploadFile(fileContents)) {
          for (const [index, row] of fileContents.entries()) {
            const studentDetails = await retrieveStudentDetails(
              row.reg_no,
              index
            );

            const classDetails = await retrieveClassDetails(
              row.class_code,
              index
            );

            if (studentDetails) {
              convertedObject = convertToPegasus(
                row,
                studentDetails,
                classDetails
              );

              convertedObjects.push(convertedObject);
            }
          }

          exportToCSV(
            convertedObjects,
            "The converted file has been downloaded.",
            "converted_to_pegasus_format"
          );

          toast.success("Your file has been succesfully converted!");
        }
      }
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when converting the file.");
    }
  };

  const convertToMMS = (
    data: IMarkMyPlace,
    studentDetails: IStudent
  ): IMarkMMS => {
    return {
      class_code: data.class_code,
      reg_no: data.reg_no,
      mark: data.override_mark ? data.override_mark : data.class_total,
      student_name: studentDetails.student_name,
      degree_level: studentDetails.degree.level,
      degree_name: studentDetails.degree.name,
    };
  };

  const convertToPegasus = (
    data: IMarkRow,
    studentDetails: IStudent,
    classDetails: IClass
  ): IMarkPegasus => {
    return {
      class_code: data.class_code,
      reg_no: data.reg_no,
      mark: data.mark,
      mark_code: "<TO FILL IN>",
      student_name: data.student_name,
      course: data.degree_name,
      degree: data.degree_level,
      degree_code: studentDetails.degree.code + "/" + studentDetails.year,
      result:
        (classDetails.credit_level >= 1 &&
          classDetails.credit_level <= 4 &&
          data.mark >= 40) ||
        (classDetails.credit_level === 5 && data.mark >= 50)
          ? "PASS"
          : "FAIL",
    };
  };

  const parseMyPlaceFile = async (): Promise<IMarkMyPlace[] | null> => {
    if (file) {
      return new Promise((resolve, reject) => {
        Papa.parse(file, {
          complete: (results) => {
            resolve(results.data as IMarkMyPlace[]);
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

  const parseMarksManagementSystemFile = async (): Promise<
    IMarkRow[] | null
  > => {
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

  const retrieveStudentDetails = async (regNo: string, index: number) => {
    try {
      if (accessToken) {
        const studentDetails = await studentService.getStudent(
          regNo,
          accessToken
        );

        if (studentDetails.statusCode !== 200) {
          toast.error(
            `Something went wrong when checking if the student exists. ${studentDetails.data}.`
          );
        }

        return studentDetails.data;
      }
    } catch (error) {
      console.error(error);

      toast.error(
        `Something went wrong when retrieving student details for Row ${
          index + 2
        }.`
      );
    }
  };

  const retrieveClassDetails = async (classCode: string, index: number) => {
    try {
      if (accessToken) {
        const classDetails = await classService.getClass(
          classCode,
          accessToken
        );

        if (classDetails.statusCode !== 200) {
          toast.error(
            `Something went wrong when checking if the class exists. ${classDetails.data}.`
          );
        }

        return classDetails.data;
      }
    } catch (error) {
      console.error(error);

      toast.error(
        `Something went wrong when retrieving class details for Row ${
          index + 2
        }.`
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

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center">
        <Card className="2xl:w-1/2 w-2/3 2xl:h-3/5 h-4/5 space-y-4 p-6 flex flex-col justify-between">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle>Convert File</CardTitle>
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
              <h2 className="text-sm text-gray-600">Supported formats: CSV</h2>
              <h2 className="text-sm text-gray-600">Maximum size: 5MB</h2>
            </div>
            <div className="flex flex-row mx-6 justify-between items-center">
              <ConvertInfoBox />
              <div className="flex flex-row space-x-4">
                <Button
                  variant="secondary"
                  className="w-20"
                  onClick={() => {
                    setFile(null);
                    setConversionType("");
                    toast.info("Convert operation has been cancelled.");
                  }}
                >
                  Cancel
                </Button>
                <ConvertSelectionCombobox
                  conversionType={conversionType}
                  conversionOpen={conversionOpen}
                  setConversionType={setConversionType}
                  setConversionOpen={setConversionOpen}
                />
                <Button
                  disabled={!file || !conversionType}
                  className="w-20"
                  onClick={() => {
                    processFile();
                    setFile(null);
                    setConversionType("");
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

export default ConvertPage;
