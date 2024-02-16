import * as React from "react";

import { InformationCircleIcon } from "@heroicons/react/24/outline";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/common/Dialog";

import { Button } from "@/components/common/Button";

const UploadInfoBox = () => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <InformationCircleIcon className="h-6 w-6 text-card-foreground cursor-pointer" />
      </DialogTrigger>
      <DialogContent>
        <DialogHeader className="space-y-4">
          <DialogTitle className="text-xl">Uploading Files</DialogTitle>
          <DialogDescription>
            To ensure a smooth and error-free experience, please adhere to the
            following guidelines:
          </DialogDescription>
          <DialogDescription>
            You can only upload one file at a time, however, if a mistake is
            made then don't worry! Simply click the "X" icon to remove the file
            you have uploaded and proceed to upload the correct one.
          </DialogDescription>
          <DialogDescription>
            Files should also not exceed 5MB, and should only be in a CSV
            format.
          </DialogDescription>
          <DialogDescription>
            In order to be able to proceed with the upload, you need to upload a
            file as well as select an upload type from the dropdown menu.
          </DialogDescription>
          <DialogDescription>
            If anything goes wrong during the upload process, you will get a
            detailed description of what needs to be altered in order for the
            data to be correctly processed.
          </DialogDescription>
        </DialogHeader>
        <DialogTrigger asChild>
          <DialogFooter>
            <Button type="submit">Close</Button>
          </DialogFooter>
        </DialogTrigger>
      </DialogContent>
    </Dialog>
  );
};

export default UploadInfoBox;
