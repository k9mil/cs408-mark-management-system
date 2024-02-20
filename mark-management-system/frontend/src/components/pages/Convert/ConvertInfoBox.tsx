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

const ConvertInfoBox = () => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <InformationCircleIcon className="h-6 w-6 text-card-foreground cursor-pointer" />
      </DialogTrigger>
      <DialogContent>
        <DialogHeader className="space-y-4">
          <DialogTitle className="text-xl">Convert Files</DialogTitle>
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
            If anything goes wrong during the conversion process, you will get a
            detailed description of what needs to be altered in order for the
            data to be correctly converted.
          </DialogDescription>
          <DialogDescription>
            You will also have the option to choose which conversion you want to
            choose, which is available in a dropdown menu to the left of the
            "Continue" button. After the conversion is done, assuming everything
            went well, the file will be downloaded and a success message will be
            displayed.
          </DialogDescription>
          <DialogDescription>
            For further information regarding the conversion process, such as
            the formats required, see the Help & Support page.
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

export default ConvertInfoBox;
