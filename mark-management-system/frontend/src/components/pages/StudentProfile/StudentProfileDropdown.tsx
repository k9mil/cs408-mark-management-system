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

export const StudentProfileDropdown = ({
  student,
  studentOpen,
  setStudent,
  setStudentOpen,
  studentList,
}: {
  student: string;
  studentOpen: boolean;
  setStudent: React.Dispatch<React.SetStateAction<string>>;
  setStudentOpen: React.Dispatch<React.SetStateAction<boolean>>;
  studentList: IUserDropdown[];
}) => {
  return (
    <div className="flex flex-col space-y-2 w-4/5">
      <Label htmlFor="student" className="text-left">
        Select a Student
      </Label>
      <Popover open={studentOpen} onOpenChange={setStudentOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            className="w-full justify-between overflow-x-hidden"
          >
            {student
              ? studentList.find(
                  (studentDropdown) => studentDropdown.value === student
                )?.label
              : "Select student..."}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-full p-0">
          <Command>
            <CommandInput placeholder="Search students..." />
            <CommandEmpty>No lecturer found.</CommandEmpty>
            <CommandGroup>
              {studentList.map((studentDropdown) => (
                <CommandItem
                  key={studentDropdown.value}
                  value={studentDropdown.label}
                  onSelect={() => {
                    setStudent(
                      studentDropdown.value === student
                        ? ""
                        : studentDropdown.value
                    );
                    setStudentOpen(false);
                  }}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      student === studentDropdown.value
                        ? "opacity-100"
                        : "opacity-0"
                    )}
                  />
                  {studentDropdown.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
};

export default StudentProfileDropdown;
