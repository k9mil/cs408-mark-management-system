import React, { useEffect, useState, useRef } from "react";

import Papa from "papaparse";

import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../AuthProvider";

import { Button } from "@/components/common/Button";
import { Card, CardHeader, CardTitle } from "@/components/common/Card";

import Sidebar from "@/components/common/Sidebar";

import { toast } from "sonner";

import { DocumentArrowUpIcon } from "@heroicons/react/24/outline";

import MarksInfoBox from "../Marks/MarksInfoBox";
import MarksUploadedFile from "../Marks/MarksUploadedFile";
import ConvertSelectionCombobox from "./ConvertSelectionCombobox";

import { IMarkMMS, IMarkMyPlace, IMarkPegasus, IMarkRow } from "@/models/IMark";
import { IStudent } from "@/models/IStudent";

import {
  generateCSVname,
  toLowerCaseIMarkMyPlace,
  toLowerCaseIMarkRow,
} from "@/utils/Utils";

import {
  validateMyPlaceFile,
  validateUploadFile,
} from "@/utils/FileUploadUtils";
import { studentService } from "@/services/StudentService";

const ConvertPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, getAccessToken } = useAuth();

  useEffect(() => {
    document.title = "Mark Management System | Convert";

    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

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

        if (
          parsedFileToLower &&
          validateMyPlaceFile(parsedFileToLower.slice(0))
        ) {
          for (const [index, row] of parsedFileToLower.slice(0).entries()) {
            const studentDetails = await retrieveStudentDetails(
              row.reg_no,
              index
            );

            if (studentDetails) {
              convertedObject = convertToMMS(row, studentDetails);
              convertedObjects.push(convertedObject);
            }
          }

          exportToCSV(convertedObjects);

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

        if (
          parsedFileToLower &&
          validateUploadFile(parsedFileToLower.slice(0))
        ) {
          for (const [index, row] of parsedFileToLower.slice(0).entries()) {
            convertedObject = convertToPegasus(row);
            convertedObjects.push(convertedObject);
          }

          exportToCSV(convertedObjects);

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

  const convertToPegasus = (data: IMarkRow): IMarkPegasus => {
    return {
      class_code: data.class_code,
      reg_no: data.reg_no,
      mark: data.mark,
      mark_code: "<TO FILL IN>",
      student_name: data.student_name,
      course: data.degree_name,
      degree: data.degree_level,
      degree_code: "<UNKNOWN>",
      result: "<TO FILL IN>",
    };
  };

  const exportToCSV = (dataToExport: IMarkMMS[] | IMarkPegasus[]) => {
    try {
      const fileName = generateCSVname("converted_to");

      if (dataToExport.length < 1) {
        toast.info("Nothing to export.");

        return;
      }

      const csv = Papa.unparse(dataToExport);

      const csvDataAsBlob = new Blob([csv], {
        type: "text/csv;charset=utf-8;",
      });

      const csvURL = window.URL.createObjectURL(csvDataAsBlob);
      const csvElement = document.createElement("a");

      csvElement.href = csvURL;
      csvElement.setAttribute("download", fileName);
      csvElement.click();

      toast.success("The converted file has been downloaded.");
    } catch (error) {
      toast.error("Something went wrong when exporting this table to CSV.");
    }
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

  const retrieveStudentDetails = async (
    studentRegNo: string,
    index: number
  ) => {
    try {
      if (accessToken) {
        const studentDetails = await studentService.getStudent(
          studentRegNo,
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

  /**
   * Validates the size & type of the file uploaded. If the file is not a CSV or >= 5MB, then an error + false is returned.
   * @param file - The file uploaded by the user.
   * @returns A boolean, true if it passes all validation and false if it fails at least one.
   */
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
        <Card className="2xl:w-1/2 xl:w-2/3 2xl:h-3/5 xl:h-4/5 space-y-4 p-6 flex flex-col justify-between">
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
              <h2 className="text-sm text-gray-400">Supported formats: CSV</h2>
              <h2 className="text-sm text-gray-400">Maximum size: 5MB</h2>
            </div>
            <div className="flex flex-row mx-6 justify-between items-center">
              <MarksInfoBox />
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
