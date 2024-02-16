import * as React from "react";

import { Button } from "@/components/common/Button";

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

export const UploadSelectionCombobox = ({
  uploadType,
  uploadOpen,
  setUploadType,
  setUploadOpen,
}: {
  uploadType: string;
  uploadOpen: boolean;
  setUploadType: React.Dispatch<React.SetStateAction<string>>;
  setUploadOpen: React.Dispatch<React.SetStateAction<boolean>>;
}) => {
  const uploadList = [
    {
      value: "student_marks",
      label: "Student Marks",
    },
    {
      value: "personal_circumstances",
      label: "Personal Circumstances",
    },
  ];

  return (
    <Popover open={uploadOpen} onOpenChange={setUploadOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          className="w-[250px] justify-between"
        >
          {uploadType
            ? uploadList.find((uploadItem) => uploadItem.value === uploadType)
                ?.label
            : "Select conversion..."}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Search upload type..." />
          <CommandEmpty>No conversions found.</CommandEmpty>
          <CommandGroup>
            {uploadList.map((uploadItem) => (
              <CommandItem
                key={uploadItem.value}
                value={uploadItem.value}
                onSelect={(currentValue) => {
                  setUploadType(
                    currentValue === uploadType ? "" : currentValue
                  );
                  setUploadOpen(false);
                }}
              >
                <Check
                  className={cn(
                    "mr-2 h-4 w-4",
                    uploadType === uploadItem.value
                      ? "opacity-100"
                      : "opacity-0"
                  )}
                />
                {uploadItem.label}
              </CommandItem>
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  );
};

export default UploadSelectionCombobox;
