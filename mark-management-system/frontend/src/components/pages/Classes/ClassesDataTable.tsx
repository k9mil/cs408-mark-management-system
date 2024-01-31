import React, { useState } from "react";

import { Button } from "@/components/common/Button";

import { ClassesModalAdminView } from "./ClassesModalAdminView";
import { ClassesModalLecturerView } from "./ClassModalLecturerView";

import { useAuth } from "@/AuthProvider";

import { formatLecturerName, getNumOfStudents } from "@/utils/ClassUtils";

import {
  ColumnDef,
  Row,
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

import { IUser } from "@/models/IUser";
import { IClass } from "@/models/IClass";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  lecturers: IUser[];
  accessToken: string | null;
  classData: () => Promise<void>;
  lecturerData: () => Promise<void>;
}

export function ClassesDataTable<TData, TValue>({
  columns,
  data,
  lecturers,
  classData,
  lecturerData,
  accessToken,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [openDialogRowId, setOpenDialogRowId] = useState<string | null>(null);
  const [selectedRow, setSelectedRow] = useState<Row<TData> | null>(null);

  const { isAdmin, isLecturer } = useAuth();

  const handleRowClick = (row: Row<TData>) => {
    setOpenDialogRowId(row.id);
    setSelectedRow(row);
  };

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
                    className="cursor-pointer hover:bg-gray-200"
                    data-state={row.getIsSelected() && "selected"}
                    onClick={() => {
                      handleRowClick(row);
                    }}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {cell.column.id === "lecturer"
                          ? formatLecturerName(
                              (cell.row.original as IClass).lecturer
                            )
                          : cell.column.id === "number_of_students"
                          ? getNumOfStudents(
                              (cell.row.original as IClass).students
                            )
                          : flexRender(
                              cell.column.columnDef.cell,
                              cell.getContext()
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
          {openDialogRowId !== null && isAdmin === true ? (
            <ClassesModalAdminView
              row={selectedRow}
              openDialogRowId={openDialogRowId}
              setOpenDialogRowId={setOpenDialogRowId}
              lecturers={lecturers}
              classData={classData}
              lecturerData={lecturerData}
              accessToken={accessToken}
            />
          ) : null}
          {openDialogRowId !== null &&
          selectedRow &&
          isLecturer === true &&
          isAdmin === false ? (
            <ClassesModalLecturerView
              row={selectedRow}
              openDialogRowId={openDialogRowId}
              setOpenDialogRowId={setOpenDialogRowId}
            />
          ) : null}
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
