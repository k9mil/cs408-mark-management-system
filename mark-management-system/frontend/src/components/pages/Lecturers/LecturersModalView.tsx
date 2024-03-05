import * as React from "react";

import { Button } from "@/components/common/Button";
import { Label } from "@/components/common/Label";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/common/Dialog";

import { IClassUploaded } from "@/models/IClass";
import { ILecturer } from "@/models/IUser";

export const LecturersModalView = ({
  row,
  openDialogRowId,
  setOpenDialogRowId,
}: {
  row: ILecturer;
  openDialogRowId: string | null;
  setOpenDialogRowId: (id: string | null) => void;
}) => {
  return (
    <Dialog
      open={openDialogRowId === row.id.toString()}
      onOpenChange={(open) => {
        if (!open) setOpenDialogRowId(null);
      }}
    >
      <DialogContent>
        <DialogHeader className="space-y-4">
          <DialogTitle className="text-xl">
            {row.first_name} {row.last_name} — View
          </DialogTitle>
          {row.classes && row.classes.length !== 0 ? (
            <DialogDescription className="max-w-md">
              Information about {row.first_name} {row.last_name} and their
              classes. Click done when you're finished.
            </DialogDescription>
          ) : null}
        </DialogHeader>
        {row.classes && row.classes.length !== 0 ? (
          <div className="grid grid-cols-2 gap-x-32 gap-y-8 mt-6">
            {row.classes.map((class_: IClassUploaded) => (
              <div key={class_.code} className="flex flex-row justify-between">
                <Label className="font-extrabold flex justify-self-center self-center">
                  {class_.code}
                </Label>
                {class_.is_uploaded === true ? (
                  <div className="rounded-md py-2 px-2 bg-green-100 flex justify-center items-center">
                    <Label className="text-green-800 font-semibold text-center flex justify-center items-center">
                      Uploaded
                    </Label>
                  </div>
                ) : (
                  <div className="rounded-md py-2 px-2 bg-red-100 flex justify-center items-center">
                    <Label className="text-red-800 font-semibold text-center flex justify-center items-center">
                      Upload Due
                    </Label>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <DialogDescription className="max-w-md">
            {row.first_name} {row.last_name} is assigned to no classes,
            therefore no information exists.
          </DialogDescription>
        )}
        <DialogTrigger asChild>
          <DialogFooter className="flex flex-row sm:justify-end mt-4">
            <Button type="submit" onClick={() => {}}>
              Done
            </Button>
          </DialogFooter>
        </DialogTrigger>
      </DialogContent>
    </Dialog>
  );
};

export default LecturersModalView;
