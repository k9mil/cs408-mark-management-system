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

export const ClassesModalLecturerView = ({
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
            Information about the {row.original.code} class. Click done when
            you're finished.
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
                defaultValue={row.original.name}
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
                defaultValue={row.original.code}
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
                defaultValue={row.original.credit}
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
                defaultValue={row.original.credit_level}
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
                value={row.original.students.length}
                disabled
              />
            </div>
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
