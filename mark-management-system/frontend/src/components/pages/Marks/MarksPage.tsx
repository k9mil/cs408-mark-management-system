import React, { useState, useEffect, useRef } from "react";

import Papa from "papaparse";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import { Button } from "@/components/common/Button";

import Sidebar from "../../common/Sidebar";

import MarksInfoBox from "./MarksInfoBox";
import MarksUploadedFile from "./MarksUploadedFile";

import { IMarkRow } from "../../../models/IMark";

import { classService } from "../../../services/ClassService";
import { studentService } from "../../../services/StudentService";
import { markService } from "../../../services/MarkService";
import { degreeService } from "../../../services/DegreeService";

import { toast } from "sonner";

import { DocumentArrowUpIcon } from "@heroicons/react/24/outline";

import { Card, CardHeader, CardTitle } from "@/components/common/Card";

const MarksPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, getAccessToken } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  const filePickedLocal = useRef(null);

  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const accessToken = getAccessToken();

  const uploadMarks = async () => {
    try {
      if (accessToken) {
        const parsedFile = await parseFileContents();

        if (parsedFile) {
          parsedFile.splice(-1, 1);

          parsedFile.forEach((row: IMarkRow) => {
            checkDegreeExists(row.DEGREE_NAME);
            checkClassExists(row.CLASS_CODE);
            checkStudentExists(row.REG_NO);
            checkMarkExists(row.UNIQUE_CODE);
          });
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

  const checkDegreeExists = async (degreeName: string) => {
    try {
      if (accessToken) {
        const degreeDetails = await degreeService.getDegree(
          degreeName,
          accessToken
        );

        if (!degreeDetails) {
          toast.error(
            "Something went wrong when uploading the marks. One of the provided degrees does not exist."
          );
        }
      }
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when uploading the marks.");
    }
  };

  const checkClassExists = async (classCode: string) => {
    try {
      if (accessToken) {
        const classDetails = await classService.getClass(
          classCode,
          accessToken
        );

        if (!classDetails) {
          toast.error(
            "Something went wrong when uploading the marks. One of the provided classes does not exist."
          );
        }
      }
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when uploading the marks.");
    }
  };

  const checkStudentExists = async (studentRegNo: string) => {
    try {
      if (accessToken) {
        const studentDetails = await studentService.getStudent(
          studentRegNo,
          accessToken
        );

        if (!studentDetails) {
          toast.error(
            "Something went wrong when uploading the marks. One of the provided students does not exist."
          );
        }
      }
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when uploading the marks.");
    }
  };

  const checkMarkExists = async (markUniqueCode: string) => {
    try {
      if (accessToken) {
        const markDetails = await markService.getMark(
          markUniqueCode,
          accessToken
        );

        if (markDetails) {
          toast.error(
            "Something went wrong when uploading the marks. One of the marks has already been uploaded."
          );
        }
      }
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when uploading the marks.");
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

    if (e.dataTransfer.files) {
      setFile(e.dataTransfer.files[0]);

      toast.success("Your file has been succesfully uploaded!");
    }
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    preventEventDefaults(e);
    setIsDragging(false);
  };

  const handleFileLocal = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);

      toast.success("Your file has been successfully uploaded!");
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
          <div className="h-1/4 flex flex-col justify-end space-y-2">
            <div className="flex flex-row justify-between mx-6">
              <h2 className="text-sm text-gray-400">Supported formats: CSV</h2>
              <h2 className="text-sm text-gray-400">Maximum size: 5MB</h2>
            </div>
            <div className="flex flex-row mx-6 justify-between items-center">
              <MarksInfoBox file={file} setFile={setFile} />
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
