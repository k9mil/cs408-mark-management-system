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

export const ConvertSelectionCombobox = ({
  conversionType,
  conversionOpen,
  setConversionType,
  setConversionOpen,
}: {
  conversionType: string;
  conversionOpen: boolean;
  setConversionType: React.Dispatch<React.SetStateAction<string>>;
  setConversionOpen: React.Dispatch<React.SetStateAction<boolean>>;
}) => {
  const conversionList = [
    {
      value: "myplacetomms",
      label: "MyPlace to MMS",
    },
    {
      value: "mmstopegasus",
      label: "MMS to Pegasus",
    },
  ];

  return (
    <Popover open={conversionOpen} onOpenChange={setConversionOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          className="w-[200px] justify-between"
        >
          {conversionType
            ? conversionList.find(
                (conversionItem) => conversionItem.value === conversionType
              )?.label
            : "Select conversion..."}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Search framework..." />
          <CommandEmpty>No conversions found.</CommandEmpty>
          <CommandGroup>
            {conversionList.map((conversionItem) => (
              <CommandItem
                key={conversionItem.value}
                value={conversionItem.value}
                onSelect={(currentValue) => {
                  setConversionType(
                    currentValue === conversionType ? "" : currentValue
                  );
                  setConversionOpen(false);
                }}
              >
                <Check
                  className={cn(
                    "mr-2 h-4 w-4",
                    conversionType === conversionItem.value
                      ? "opacity-100"
                      : "opacity-0"
                  )}
                />
                {conversionItem.label}
              </CommandItem>
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  );
};

export default ConvertSelectionCombobox;
