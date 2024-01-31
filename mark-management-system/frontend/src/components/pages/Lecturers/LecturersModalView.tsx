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

export const LecturersModalView = ({
  row,
  openDialogRowId,
  setOpenDialogRowId,
}: {
  row: Row<TData>;
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
          <DialogTitle className="text-xl">
            {row.original.first_name} {row.original.last_name} — View
          </DialogTitle>
          {row.original.classes && row.original.classes.length !== 0 ? (
            <DialogDescription className="max-w-md">
              Information about {row.original.first_name}{" "}
              {row.original.last_name} and their classes. Click done when you're
              finished.
            </DialogDescription>
          ) : null}
        </DialogHeader>
        {row.original.classes && row.original.classes.length !== 0 ? (
          <div className="grid grid-cols-2 gap-x-32 gap-y-8 mt-6">
            {row.original.classes.map((class_: IClassUploaded) => (
              <div key={class_.code} className="flex flex-row space-x-2">
                <Label className="font-bold">{class_.code}</Label>
                {class_.is_uploaded === true ? (
                  <Label className="text-green-500 font-bold">Uploaded</Label>
                ) : (
                  <Label className="text-red-500 font-bold">Due</Label>
                )}
              </div>
            ))}
          </div>
        ) : (
          <DialogDescription className="max-w-md">
            {row.original.first_name} {row.original.last_name} is assigned to no
            classes, therefore no information exists.
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
