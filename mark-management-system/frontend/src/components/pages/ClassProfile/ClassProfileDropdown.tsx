import * as React from "react";

import { Button } from "@/components/common/Button";
import { Label } from "@/components/common/Label";

import { Check, ChevronsUpDown } from "lucide-react";
import { cn } from "@/lib/utils";

import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "@/components/common/Command";

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/common/Popover";

import { IUserDropdown } from "../../../models/IUser";

export const ClassProfileDropdown = ({
  class_,
  classOpen,
  setClass,
  setClassOpen,
  classList,
}: {
  class_: string;
  classOpen: boolean;
  setClass: React.Dispatch<React.SetStateAction<string>>;
  setClassOpen: React.Dispatch<React.SetStateAction<boolean>>;
  classList: IUserDropdown[];
}) => {
  return (
    <div className="flex flex-col space-y-2 w-fit">
      <Label htmlFor="class_" className="text-left">
        Select a Class
      </Label>
      <Popover open={classOpen} onOpenChange={setClassOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            className="w-full justify-between overflow-x-hidden"
          >
            {class_
              ? classList.find(
                  (classDropdown) => classDropdown.value === class_
                )?.label
              : "Select class..."}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-full p-0">
          <Command>
            <CommandInput placeholder="Search classes..." />
            <CommandEmpty>No class found.</CommandEmpty>
            <CommandGroup>
              {classList.map((classDropdown) => (
                <CommandItem
                  key={classDropdown.value}
                  value={classDropdown.label}
                  onSelect={() => {
                    setClass(
                      classDropdown.value === class_ ? "" : classDropdown.value
                    );
                    setClassOpen(false);
                  }}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      class_ === classDropdown.value
                        ? "opacity-100"
                        : "opacity-0"
                    )}
                  />
                  {classDropdown.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
};

export default ClassProfileDropdown;
