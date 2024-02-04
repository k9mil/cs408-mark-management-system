import React, { useEffect, useState } from "react";

import { ClassesLecturerDropdown } from "./ClassesLecturerDropdown";

import { Button } from "@/components/common/Button";
import { Label } from "@/components/common/Label";
import { Input } from "@/components/common/Input";

import { toast } from "sonner";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/common/Dialog";

import { IClass, IClassWithId } from "@/models/IClass";
import { IUser, IUserDropdown } from "@/models/IUser";

import { classService } from "@/services/ClassService";

import { validateClassDetails } from "@/utils/ClassUtils";

export const ClassesModalAdminView = ({
  row,
  openDialogRowId,
  setOpenDialogRowId,
  lecturers,
  classData,
  lecturerData,
  accessToken,
}: {
  row: IClass;
  openDialogRowId: string | null;
  setOpenDialogRowId: (id: string | null) => void;
  lecturers: IUser[];
  classData: () => Promise<void>;
  lecturerData: () => Promise<void>;
  accessToken: string | null;
}) => {
  const [name, setName] = useState(row.name);
  const [originalCode] = useState(row.code);
  const [code, setCode] = useState(row.code);
  const [credits, setCredits] = useState(row.credit);
  const [creditLevel, setCreditLevel] = useState(row.credit_level);

  const [lecturerOpen, setLecturerOpen] = React.useState(false);
  const [lecturer, setLecturer] = React.useState("");

  const [lecturerList, setLecturerList] = React.useState<
    IUserDropdown[] | null
  >(null);

  useEffect(() => {
    if (lecturers && Array.isArray(lecturers)) {
      const mappedLecturers = lecturers.map((user: IUser) => ({
        value: user.id.toString(),
        label: `${user.first_name} ${user.last_name}`,
      }));

      setLecturerList(mappedLecturers);

      const defaultLecturer = lecturers.find(
        (lecturer) =>
          lecturer.first_name === row.lecturer.first_name &&
          lecturer.last_name === row.lecturer.last_name
      );

      if (defaultLecturer) {
        setLecturer(defaultLecturer.id.toString());
      }
    }
  }, [lecturers, row]);

  const deleteClass = async (classId: number) => {
    try {
      if (accessToken) {
        await classService.deleteClass(classId, accessToken);
        toast.success("Class was deleted successfully!");
      }

      lecturerData();
      classData();
      setOpenDialogRowId(null);
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when deleting the class.");
    }
  };

  const editClass = async (classDetails: IClassWithId) => {
    try {
      if (accessToken) {
        await classService.editClass(classDetails, accessToken);
        toast.success("Class was edited successfully!");
      }

      lecturerData();
      classData();
      setOpenDialogRowId(null);
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when editing the class details.");
    }
  };

  return (
    <Dialog
      open={openDialogRowId === row.id.toString()}
      onOpenChange={(open) => {
        if (!open) setOpenDialogRowId(null);
      }}
    >
      <DialogContent>
        <DialogHeader className="space-y-4">
          <DialogTitle className="text-xl">CS408 — View</DialogTitle>
          <DialogDescription className="max-w-md">
            Information about the {row.code} class. Click done when you're
            finished.
          </DialogDescription>
        </DialogHeader>
        <div className="flex flex-row justify-between">
          <div className="space-y-4">
            <div>
              <Label htmlFor="name" className="text-right">
                Name
              </Label>
              <Input
                id="name"
                className="col-span-3"
                defaultValue={row.name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="code" className="text-right">
                Code
              </Label>
              <Input
                id="name"
                className="col-span-3"
                defaultValue={row.code}
                onChange={(e) => setCode(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="credits" className="text-right">
                Credits
              </Label>
              <Input
                id="name"
                className="col-span-3"
                defaultValue={row.credit}
                onChange={(e) => setCredits(+e.target.value)}
              />
            </div>
          </div>
          <div className="space-y-4">
            <div>
              <Label htmlFor="creditLevel" className="text-right">
                Credit Level
              </Label>
              <Input
                id="name"
                className="col-span-3"
                defaultValue={row.credit_level}
                onChange={(e) => setCreditLevel(+e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="numberOfStudents" className="text-right">
                Number of Students
              </Label>
              <Input
                id="name"
                className="col-span-3"
                value={row.students.length}
                disabled
              />
            </div>
            {lecturerList !== null && lecturerList.length !== 0 ? (
              <ClassesLecturerDropdown
                lecturer={lecturer}
                lecturerOpen={lecturerOpen}
                setLecturer={setLecturer}
                setLecturerOpen={setLecturerOpen}
                lecturerList={lecturerList}
              />
            ) : null}
          </div>
        </div>
        <DialogFooter className="flex flex-row sm:justify-between mt-8">
          <Button
            type="submit"
            variant="destructive"
            onClick={() => {
              deleteClass(row.id);
            }}
          >
            Remove
          </Button>
          <Button
            type="submit"
            onClick={() => {
              const classDetails: IClassWithId = {
                id: +row.id,
                name: name,
                code: code,
                original_code: originalCode,
                credit: +credits,
                credit_level: +creditLevel,
                lecturer_id: +lecturer,
              };

              if (validateClassDetails(classDetails)) {
                editClass(classDetails);
              }
            }}
          >
            Save changes
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default ClassesModalAdminView;
