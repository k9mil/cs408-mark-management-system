import * as React from "react";

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

export const StudentsModal = ({
  row,
  openDialogRowId,
  setOpenDialogRowId,
}: {
  row: any;
  openDialogRowId: string | null;
  setOpenDialogRowId: (id: string | null) => void;
}) => {
  return (
    <Dialog
      open={openDialogRowId === row.id}
      onOpenChange={(open) => {
        if (!open) setOpenDialogRowId(null);
      }}
    >
      <DialogContent>
        <DialogHeader className="space-y-4">
          <DialogTitle className="text-xl">CS408 — View</DialogTitle>
          <DialogDescription className="max-w-md">
            Information about the mark for {row.original.student_name}. Click
            save when you're finished.
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
                defaultValue={row.original.student_name}
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
                defaultValue={row.original.class_code}
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
                defaultValue={row.original.reg_no}
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
                defaultValue={row.original.degree_level}
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
                defaultValue={row.original.degree_name}
                disabled
              />
            </div>
            <div>
              <Label htmlFor="mark" className="text-right">
                Mark
              </Label>
              <Input
                id="mark"
                className="col-span-3"
                defaultValue={row.original.mark}
              />
            </div>
          </div>
        </div>
        <DialogFooter className="flex flex-row sm:justify-between mt-8">
          <Button
            type="submit"
            variant="destructive"
            onClick={() => {
              setOpenDialogRowId(null);
            }}
          >
            Remove
          </Button>
          <Button
            type="submit"
            onClick={() => {
              setOpenDialogRowId(null);
            }}
          >
            Save changes
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default StudentsModal;
