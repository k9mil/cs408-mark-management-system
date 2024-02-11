import React, { useState, useEffect } from "react";

import { Button } from "@/components/common/Button";
import { Label } from "@/components/common/Label";
import { Input } from "@/components/common/Input";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/common/Dialog";

import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/common/Card";

import { markService } from "@/services/MarkService";

import { toast } from "sonner";

import { validateMarkDetailsOnEdit } from "@/utils/StudentUtils";

import { IMarkEdit, IMarkRow } from "@/models/IMark";

export const StudentsModal = ({
  row,
  openDialogRowId,
  setOpenDialogRowId,
  accessToken,
  marksData,
}: {
  row: IMarkRow;
  openDialogRowId: string | null;
  setOpenDialogRowId: (id: string | null) => void;
  accessToken: string | null;
  marksData: () => Promise<void>;
}) => {
  const [hasRendered, setHasRendered] = useState<boolean>(false);
  const [studentMarks, setStudentMarks] = useState<IMarkRow[]>([]);
  const [activeTab, setActiveTab] = useState("class");
  const [mark, setMark] = useState(row.mark ? +row.mark : null);

  useEffect(() => {
    if (
      studentMarks &&
      studentMarks.length !== 0 &&
      activeTab === "overall" &&
      !hasRendered
    ) {
      setHasRendered(true);
    }
  }, [studentMarks, activeTab, hasRendered]);

  const deleteMark = async (uniqueCode: string) => {
    try {
      if (accessToken) {
        await markService.deleteMark(uniqueCode, accessToken);
        toast.success("Mark was deleted successfully!");
      }

      marksData();
      setOpenDialogRowId(null);
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when deleting the mark.");
    }
  };

  const editMark = async (markDetails: IMarkEdit) => {
    try {
      if (accessToken) {
        await markService.editMark(markDetails, accessToken);
        toast.success("Mark was edited successfully!");
      }

      marksData();
      setOpenDialogRowId(null);
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when editing the mark details.");
    }
  };

  useEffect(() => {
    const retrieveStudentMarks = async () => {
      try {
        if (accessToken) {
          const result = await markService.getMarksForStudent(
            row.reg_no,
            accessToken
          );

          setStudentMarks(result);
        }
      } catch (error) {
        console.error(error);
      }
    };

    retrieveStudentMarks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Dialog
      open={openDialogRowId === row.id.toString()}
      onOpenChange={(open) => {
        if (!open) setOpenDialogRowId(null);
      }}
    >
      <DialogContent className="2xl:w-1/2 2xl:h-1/2 xl:h-3/5 xl:w-3/5 m-0">
        <DialogHeader className="space-y-4">
          <DialogTitle className="flex flex-row space-x-4 justify-around">
            <h2
              className={`text-lg hover:cursor-pointer ${
                activeTab == "class" ? "underline font-semibold" : "font-medium"
              }`}
              onClick={() => setActiveTab("class")}
            >
              Class View
            </h2>
            <h2
              className={`text-lg hover:cursor-pointer ${
                activeTab == "overall"
                  ? "underline font-semibold"
                  : "font-medium"
              }`}
              onClick={() => setActiveTab("overall")}
            >
              Overall View
            </h2>
          </DialogTitle>
          {activeTab === "class" ? (
            <DialogDescription className="max-w-md">
              Information about the mark for {row.student_name} for{" "}
              {row.class_code}. Click save when you're finished.
            </DialogDescription>
          ) : (
            <DialogDescription className="max-w-md">
              Information about overall marks in the system for{" "}
              {row.student_name}. Click done when you're finished.
            </DialogDescription>
          )}
        </DialogHeader>
        {activeTab === "class" ? (
          <div className="flex flex-row justify-between">
            <div className="space-y-4">
              <div>
                <Label htmlFor="name" className="text-right">
                  Name
                </Label>
                <Input
                  id="name"
                  className="col-span-3"
                  defaultValue={row.student_name}
                  disabled
                />
              </div>
              <div>
                <Label htmlFor="code" className="text-right">
                  Code
                </Label>
                <Input
                  id="name"
                  className="col-span-3"
                  defaultValue={row.class_code}
                  disabled
                />
              </div>
              <div>
                <Label htmlFor="code" className="text-right">
                  Registration Number
                </Label>
                <Input
                  id="name"
                  className="col-span-3"
                  defaultValue={row.reg_no}
                  disabled
                />
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <Label htmlFor="degreeLevel" className="text-right">
                  Degree Level
                </Label>
                <Input
                  id="degreeLevel"
                  className="col-span-3"
                  defaultValue={row.degree_level}
                  disabled
                />
              </div>
              <div>
                <Label htmlFor="degreeName" className="text-right">
                  Degree Name
                </Label>
                <Input
                  id="degreeName"
                  className="col-span-3"
                  defaultValue={row.degree_name}
                  disabled
                />
              </div>
              <div>
                <Label htmlFor="mark" className="text-right">
                  Mark
                </Label>
                <Input
                  id="mark"
                  type="text"
                  className="col-span-3"
                  defaultValue={row.mark}
                  onChange={(e) => {
                    setMark(e.target.value === "" ? null : +e.target.value);
                  }}
                />
              </div>
            </div>
          </div>
        ) : hasRendered ? (
          <div className="grid grid-cols-3 gap-y-3 justify-items-center overflow-y-scroll py-4 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
            {studentMarks.map((mark_row: IMarkRow) => (
              <Card className="flex flex-col w-28 h-28 space-y-2 justify-center items-center shadow-lg">
                <CardHeader className="flex flex-row justify-between items-center p-0">
                  <CardTitle className="text-2xl font-bold">
                    {mark_row.class_code}
                  </CardTitle>
                </CardHeader>
                <CardDescription>
                  <h2 className="text-sm">Mark: {mark_row.mark}</h2>
                </CardDescription>
              </Card>
            ))}
          </div>
        ) : null}
        {activeTab === "class" ? (
          <DialogFooter className="flex flex-row sm:justify-between items-end">
            <Button
              type="submit"
              variant="destructive"
              onClick={() => {
                deleteMark(row.unique_code);
              }}
            >
              Remove
            </Button>
            <Button
              type="submit"
              onClick={() => {
                const markDetails: IMarkEdit = {
                  unique_code: row.unique_code,
                  mark: mark === null ? null : +mark,
                };

                if (validateMarkDetailsOnEdit(markDetails)) {
                  editMark(markDetails);
                }
              }}
            >
              Save changes
            </Button>
          </DialogFooter>
        ) : (
          <DialogFooter className="flex sm:self-justify-end">
            <Button
              type="submit"
              onClick={() => {
                setOpenDialogRowId(null);
              }}
            >
              Done
            </Button>
          </DialogFooter>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default StudentsModal;
