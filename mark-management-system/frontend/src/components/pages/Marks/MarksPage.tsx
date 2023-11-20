import * as React from "react";

import Sidebar from "../../common/Sidebar";

import {
  DocumentArrowUpIcon,
  XMarkIcon,
  InformationCircleIcon,
} from "@heroicons/react/24/outline";

import { Card, CardHeader, CardTitle } from "@/components/common/Card";
import { Button } from "@/components/common/Button";

const MarksPage = () => {
  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center">
        <Card className="w-1/2 h-3/5 space-y-4 p-2">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle>Upload Marks</CardTitle>
            <XMarkIcon className="h-6 w-6 text-card-foreground" />
          </CardHeader>
          <div className="mx-6 rounded-md border-2 border-dashed border-gray-300 p-28 flex flex-col justify-center items-center space-y-8">
            <DocumentArrowUpIcon className="h-16 w-16 text-card-foreground" />
            <h2 className="text-card-foreground font-semibold">
              Drag and Drop file here or{" "}
              <span className="underline font-bold underline-offset-4">
                Choose File
              </span>
            </h2>
          </div>
          <div className="flex flex-row justify-between mx-6">
            <h2 className="text-gray-400">Supported formats: CSV</h2>
            <h2 className="text-gray-400">Maximum size: 5MB</h2>
          </div>
          <div className="flex flex-row mx-6 justify-between items-center">
            <InformationCircleIcon className="h-6 w-6 text-card-foreground cursor-pointer" />
            <div className="flex flex-row space-x-4">
              <Button variant="secondary" className="w-20">
                Cancel
              </Button>
              <Button className="w-20">Next</Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default MarksPage;
