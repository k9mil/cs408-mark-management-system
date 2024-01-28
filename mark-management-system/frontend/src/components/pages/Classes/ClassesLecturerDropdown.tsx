import React, { useEffect } from "react";

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

export const ClassesLecturerDropdown = ({
  lecturer,
  lecturerOpen,
  setLecturer,
  setLecturerOpen,
  lecturerList,
}: {
  lecturer: string;
  lecturerOpen: boolean;
  setLecturer: React.Dispatch<React.SetStateAction<string>>;
  setLecturerOpen: React.Dispatch<React.SetStateAction<boolean>>;
  lecturerList: IUserDropdown[];
}) => {
  useEffect(() => {
    console.log(lecturerList);
    console.log(lecturer);
  }, [lecturerList]);

  return (
    <div className="flex flex-col space-y-2">
      <Label htmlFor="lecturer" className="text-left">
        Lecturer
      </Label>
      <Popover open={lecturerOpen} onOpenChange={setLecturerOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-[200px] justify-between"
          >
            {lecturer
              ? lecturerList.find(
                  (lecturerDropdown) => lecturerDropdown.value === lecturer
                )?.label
              : "Select lecturer..."}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[200px] p-0">
          <Command>
            <CommandInput placeholder="Search lecturers..." />
            <CommandEmpty>No lecturer found.</CommandEmpty>
            <CommandGroup>
              {lecturerList.map((lecturerDropdown) => (
                <CommandItem
                  key={lecturerDropdown.value}
                  value={lecturerDropdown.label}
                  onSelect={() => {
                    setLecturer(
                      lecturerDropdown.value === lecturer
                        ? ""
                        : lecturerDropdown.value
                    );
                    setLecturerOpen(false);
                  }}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      lecturer === lecturerDropdown.value
                        ? "opacity-100"
                        : "opacity-0"
                    )}
                  />
                  {lecturerDropdown.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
};

export default ClassesLecturerDropdown;
