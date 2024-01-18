import React, { useEffect, useState } from "react";

import { Check, ChevronsUpDown } from "lucide-react";

import { cn } from "@/lib/utils";

import { Button } from "@/components/common/Button";
import { Label } from "@/components/common/Label";
import { Input } from "@/components/common/Input";

import {
  ColumnDef,
  SortingState,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";

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

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/common/Table";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/common/Dialog";

import { User } from "./ClassesColumns";
import { userService } from "../../../services/UserService";

import { ClassDTO, ClassDTOWithId } from "./ClassesColumns";
import { classService } from "../../../services/ClassService";

import { toast } from "sonner";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

function formatLecturerName(lecturer: User) {
  return `${lecturer.first_name} ${lecturer.last_name}`;
}

function getNumOfStudents(students: Array<User>) {
  if (students) return students.length;
  return 0;
}

export function ClassesDataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [openDialogRowId, setOpenDialogRowId] = useState<string | null>(null);

  const [lecturerOpen, setLecturerOpen] = React.useState(false);
  const [lecturer, setLecturer] = React.useState("");
  const [lecturers, setLecturers] = useState<User[]>([]);

  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [credits, setCredits] = useState(0);
  const [creditLevel, setCreditLevel] = useState(0);

  useEffect(() => {
    const lecturerData = async () => {
      try {
        const result = await userService.getUsers();
        setLecturers(result);
      } catch (error) {
        console.error(error);
      }
    };

    lecturerData();
  }, []);

  const deleteClass = async (classId: number) => {
    try {
      await classService.deleteClass(classId);
      toast.success("Class was deleted successfully!");
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when deleting the class.");
    }
  };

  const editClass = async (classDetails: ClassDTO) => {
    try {
      await classService.editClass(classDetails);
      toast.success("Class was edited successfully!");
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when editing the class details.");
    }
  };

  const lecturerList = lecturers.map((user) => ({
    value: user.id.toString(),
    label: `${user.first_name} ${user.last_name}`,
  }));

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onSortingChange: setSorting,
    getSortedRowModel: getSortedRowModel(),
    state: {
      sorting,
    },
  });

  return (
    <>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <>
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() && "selected"}
                    onClick={() => {
                      setOpenDialogRowId(row.id);
                    }}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {cell.column.id === "lecturer"
                          ? formatLecturerName(cell.row.original.lecturer)
                          : cell.column.id === "number_of_students"
                          ? getNumOfStudents(cell.row.original.students)
                          : flexRender(
                              cell.column.columnDef.cell,
                              cell.getContext()
                            )}
                      </TableCell>
                    ))}
                  </TableRow>
                  <Dialog
                    open={openDialogRowId === row.id}
                    onOpenChange={(open) => {
                      if (!open) setOpenDialogRowId(null);
                    }}
                  >
                    <DialogContent>
                      <DialogHeader className="space-y-4">
                        <DialogTitle className="text-xl">
                          CS408 — View
                        </DialogTitle>
                        <DialogDescription className="max-w-xs">
                          Information about the CS408 class. Click done when
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
                              defaultValue={row.original.name}
                              onChange={(e) => setName(e.target.value)}
                            />
                          </div>
                          <div>
                            <Label htmlFor="code" className="text-right">
                              Code
                            </Label>
                            <Input
                              id="name"
                              className="col-span-3"
                              defaultValue={row.original.code}
                              onChange={(e) => setCode(e.target.value)}
                            />
                          </div>
                          <div>
                            <Label htmlFor="credits" className="text-right">
                              Credits
                            </Label>
                            <Input
                              id="name"
                              className="col-span-3"
                              defaultValue={row.original.credit}
                              onChange={(e) => setCredits(e.target.value)}
                            />
                          </div>
                        </div>
                        <div className="space-y-4">
                          <div>
                            <Label htmlFor="creditLevel" className="text-right">
                              Credit Level
                            </Label>
                            <Input
                              id="name"
                              className="col-span-3"
                              defaultValue={row.original.credit_level}
                              onChange={(e) => setCreditLevel(e.target.value)}
                            />
                          </div>
                          <div>
                            <Label
                              htmlFor="numberOfStudents"
                              className="text-right"
                            >
                              Number of Students
                            </Label>
                            <Input
                              id="name"
                              className="col-span-3"
                              value={row.original.students.length}
                              disabled
                            />
                          </div>
                          <div className="flex flex-col space-y-2">
                            <Label htmlFor="lecturer" className="text-left">
                              Lecturer
                            </Label>
                            <Popover
                              open={lecturerOpen}
                              onOpenChange={setLecturerOpen}
                            >
                              <PopoverTrigger asChild>
                                <Button
                                  variant="outline"
                                  role="combobox"
                                  aria-expanded={open}
                                  className="w-[200px] justify-between"
                                >
                                  {lecturer
                                    ? lecturerList.find(
                                        (lecturerDropdown) =>
                                          lecturerDropdown.value === lecturer
                                      )?.label
                                    : "Select lecturer..."}
                                  <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                                </Button>
                              </PopoverTrigger>
                              <PopoverContent className="w-[200px] p-0">
                                <Command>
                                  <CommandInput placeholder="Search lecturers..." />
                                  <CommandEmpty>
                                    No lecturer found.
                                  </CommandEmpty>
                                  <CommandGroup>
                                    {lecturerList.map((lecturerDropdown) => (
                                      <CommandItem
                                        key={lecturerDropdown.value}
                                        value={lecturerDropdown.value}
                                        onSelect={(currentValue) => {
                                          setLecturer(
                                            currentValue === lecturer
                                              ? ""
                                              : currentValue
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
                        </div>
                      </div>
                      <DialogFooter className="flex flex-row sm:justify-between mt-8">
                        <Button
                          type="submit"
                          variant="destructive"
                          onClick={() => {
                            deleteClass(row.original.id);
                            setOpenDialogRowId(null);
                          }}
                        >
                          Remove
                        </Button>
                        <Button
                          type="submit"
                          onClick={() => {
                            const classDetails: ClassDTOWithId = {
                              id: +row.original.id,
                              name: name,
                              code: code,
                              credit: +credits,
                              credit_level: +creditLevel,
                              lecturer_id: +lecturer,
                            };

                            editClass(classDetails);
                            setOpenDialogRowId(null);
                          }}
                        >
                          Save changes
                        </Button>
                      </DialogFooter>
                    </DialogContent>
                  </Dialog>
                </>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          Next
        </Button>
      </div>
    </>
  );
}

export default ClassesDataTable;
