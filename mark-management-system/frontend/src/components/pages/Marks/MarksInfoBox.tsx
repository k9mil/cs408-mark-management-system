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

const MarksInfoBox = () => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <InformationCircleIcon className="h-6 w-6 text-card-foreground cursor-pointer" />
      </DialogTrigger>
      <DialogContent>
        <DialogHeader className="space-y-4">
          <DialogTitle className="text-xl">Uploading Marks</DialogTitle>
          <DialogDescription>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam
            cursus at dui eget accumsan. In magna mauris, laoreet non blandit
            rutrum, consectetur vitae erat. Nulla euismod, augue id varius
            malesuada, nunc metus fermentum enim, vel vehicula quam turpis eget
            magna.
          </DialogDescription>
          <DialogDescription>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam
            cursus at dui eget accumsan. In magna mauris, laoreet non blandit
            rutrum, consectetur vitae erat. Nulla euismod, augue id varius
            malesuada, nunc metus fermentum enim, vel vehicula quam turpis eget
            magna.
          </DialogDescription>
          <DialogDescription>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam
            cursus at dui eget accumsan.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button type="submit">Close</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default MarksInfoBox;
