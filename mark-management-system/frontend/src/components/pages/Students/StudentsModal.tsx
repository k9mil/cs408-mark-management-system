import React, { useState } from "react";

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
  const [mark, setMark] = useState(row.mark ? +row.mark : null);

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
            {row.student_name} — View
          </DialogTitle>
          <DialogDescription className="max-w-md">
            Information about the mark for {row.student_name}. Click save when
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
        <DialogFooter className="flex flex-row sm:justify-between mt-8">
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
      </DialogContent>
    </Dialog>
  );
};

export default StudentsModal;
