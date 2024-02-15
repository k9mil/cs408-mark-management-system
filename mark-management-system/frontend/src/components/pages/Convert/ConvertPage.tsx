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

import { IMarkMyPlace } from "@/models/IMark";

import { toLowerCaseIMarkMyPlace } from "@/utils/Utils";
import { validateMyPlaceFile } from "@/utils/FileUploadUtils";

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

  const convertFile = async () => {
    try {
      if (!accessToken) {
        toast.error("Access token is missing.");

        return;
      }

      if (conversionType === "myplace_to_mms") {
        const parsedFile = await parseMyPlaceFile();
        let parsedFileToLower;

        if (parsedFile) {
          parsedFileToLower = toLowerCaseIMarkMyPlace(parsedFile);
        }

        if (
          parsedFileToLower &&
          validateMyPlaceFile(parsedFileToLower.slice(0))
        ) {
          toast.success("Your file has been succesfully converted!");
        }
      }

      //   if (conversionType === "mms_to_pegasus") {
      //   }
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when converting the file.");
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
                <Button variant="secondary" className="w-20">
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
                    convertFile();
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
