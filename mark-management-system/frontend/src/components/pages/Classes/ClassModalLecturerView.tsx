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

import { IClass } from "@/models/IClass";
import { IDegree } from "@/models/IDegree";

import { classService } from "@/services/ClassService";

export const ClassesModalLecturerView = ({
  row,
  openDialogRowId,
  setOpenDialogRowId,
  accessToken,
}: {
  row: IClass;
  openDialogRowId: string | null;
  setOpenDialogRowId: (id: string | null) => void;
  accessToken: string | null;
}) => {
  const [degrees, setDegrees] = useState<IDegree[]>([]);

  const associatedDegrees = async (classCode: string) => {
    try {
      if (accessToken) {
        const result = await classService.getAssociatedDegreesForClass(
          classCode,
          accessToken
        );

        console.log(result);
        setDegrees(result);
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    associatedDegrees(row.code);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Dialog
      open={openDialogRowId === row.id.toString()}
      onOpenChange={(open) => {
        if (!open) setOpenDialogRowId(null);
      }}
    >
      <DialogContent className="max-w-2xl">
        <DialogHeader className="space-y-4">
          <DialogTitle className="text-xl">{row.code} — View</DialogTitle>
          <DialogDescription className="max-w-md">
            Information about the {row.code} class. Click done when you're
            finished.
          </DialogDescription>
        </DialogHeader>
        <div className="flex flex-row justify-between space-x-6">
          <div className="space-y-4">
            <div>
              <Label htmlFor="name" className="text-right">
                Name
              </Label>
              <Input
                id="name"
                className="col-span-3"
                defaultValue={row.name}
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
                defaultValue={row.code}
                disabled
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
                disabled
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
                disabled
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
          </div>
          <div className="space-y-4">
            <h2 className="font-bold text-sm">
              Degrees the class is associated with:
            </h2>
            {degrees && degrees.length > 0 ? (
              degrees.map((degree: IDegree) => (
                <h3 className="font-normal text-sm">
                  {degree.level} {degree.name}
                </h3>
              ))
            ) : (
              <h3 className="font-normal text-sm">
                This class is not associated with any degrees.
              </h3>
            )}
          </div>
        </div>
        <DialogFooter className="flex sm:justify-end mt-4">
          <Button
            type="submit"
            onClick={() => {
              setOpenDialogRowId(null);
            }}
          >
            Done
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default ClassesModalLecturerView;
