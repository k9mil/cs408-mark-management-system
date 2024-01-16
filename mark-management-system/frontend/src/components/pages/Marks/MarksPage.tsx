import React, { useState } from "react";

import Sidebar from "../../common/Sidebar";

import { toast } from "sonner";

import {
  DocumentArrowUpIcon,
  InformationCircleIcon,
} from "@heroicons/react/24/outline";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/common/Dialog";

import { Card, CardHeader, CardTitle } from "@/components/common/Card";
import { Button } from "@/components/common/Button";

const MarksPage = () => {
  const [isDragging, setIsDragging] = useState(false);

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

    toast.success("Your file has been succesfully uploaded!");
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    preventEventDefaults(e);
    setIsDragging(false);
  };

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center">
        <Card className="w-1/2 h-3/5 space-y-4 p-2">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle>Upload Marks</CardTitle>
            {/* <XMarkIcon className="h-6 w-6 text-card-foreground cursor-pointer" /> */}
          </CardHeader>
          <div
            className={
              "mx-6 rounded-md border-2 border-dashed border-gray-300 p-28 flex flex-col justify-center items-center space-y-8 " +
              (isDragging ? "border-primary-blue bg-slate-50" : "")
            }
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <DocumentArrowUpIcon className="h-16 w-16 text-card-foreground" />
            <h2 className="text-card-foreground font-semibold">
              Drag and Drop files here or{" "}
              <span className="underline font-bold underline-offset-4 cursor-pointer">
                Choose File
              </span>
            </h2>
          </div>
          <div className="flex flex-row justify-between mx-6">
            <h2 className="text-gray-400">Supported formats: CSV</h2>
            <h2 className="text-gray-400">Maximum size: 5MB</h2>
          </div>
          <div className="flex flex-row mx-6 justify-between items-center">
            <Dialog>
              <DialogTrigger asChild>
                <InformationCircleIcon className="h-6 w-6 text-card-foreground cursor-pointer" />
              </DialogTrigger>
              <DialogContent>
                <DialogHeader className="space-y-4">
                  <DialogTitle className="text-xl">Uploading Marks</DialogTitle>
                  <DialogDescription>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    Nullam cursus at dui eget accumsan. In magna mauris, laoreet
                    non blandit rutrum, consectetur vitae erat. Nulla euismod,
                    augue id varius malesuada, nunc metus fermentum enim, vel
                    vehicula quam turpis eget magna.
                  </DialogDescription>
                  <DialogDescription>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    Nullam cursus at dui eget accumsan. In magna mauris, laoreet
                    non blandit rutrum, consectetur vitae erat. Nulla euismod,
                    augue id varius malesuada, nunc metus fermentum enim, vel
                    vehicula quam turpis eget magna.
                  </DialogDescription>
                  <DialogDescription>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    Nullam cursus at dui eget accumsan.
                  </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                  <Button type="submit">Close</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
            <div className="flex flex-row space-x-4">
              <Button variant="secondary" className="w-20">
                Cancel
              </Button>
              <Button disabled className="w-20">
                Next
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default MarksPage;
