import React, { useEffect, useState } from "react";

import { Button } from "@/components/common/Button";

import { ClassesModal } from "./ClassesModal";
import {
  formatLecturerName,
  getNumOfStudents,
} from "../../../utils/ClassUtils";

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

import { userService } from "../../../services/UserService";
import { IUser } from "../../../models/IUser";

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
  const [lecturers, setLecturers] = useState<IUser[]>([]);

  const lecturerData = async () => {
    try {
      const result = await userService.getUsers();
      setLecturers(result);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    lecturerData();
  }, []);

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
                <React.Fragment key={row.id}>
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
                        {openDialogRowId !== null && (
                          <ClassesModal
                            row={cell.row}
                            openDialogRowId={openDialogRowId}
                            setOpenDialogRowId={setOpenDialogRowId}
                            lecturers={lecturers}
                            lecturerData={lecturerData}
                          />
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                </React.Fragment>
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
