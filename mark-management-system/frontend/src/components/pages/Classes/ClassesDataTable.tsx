import * as React from "react";

import { useState } from "react";

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

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

export function ClassesDataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [openDialogRowId, setOpenDialogRowId] = useState<string | null>(null);

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
                        {flexRender(
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
                              value={row.original.name}
                            />
                          </div>
                          <div>
                            <Label htmlFor="code" className="text-right">
                              Code
                            </Label>
                            <Input
                              id="name"
                              className="col-span-3"
                              value={row.original.code}
                            />
                          </div>
                          <div>
                            <Label htmlFor="credits" className="text-right">
                              Credits
                            </Label>
                            <Input
                              id="name"
                              className="col-span-3"
                              value={row.original.credit}
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
                              value={row.original.credit_level}
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
                              value={row.original.number_of_students}
                            />
                          </div>
                          <div>
                            <Label htmlFor="lecturer" className="text-right">
                              Lecturer
                            </Label>
                            <Input
                              id="name"
                              className="col-span-3"
                              value={row.original.lecturer.first_name}
                            />
                          </div>
                        </div>
                      </div>
                      <DialogFooter className="flex flex-row sm:justify-between mt-8">
                        <Button type="submit" variant="destructive">
                          Remove
                        </Button>
                        <Button type="submit">Save changes</Button>
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
