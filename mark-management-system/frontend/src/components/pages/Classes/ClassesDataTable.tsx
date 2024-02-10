import React, { useState } from "react";

import { Button } from "@/components/common/Button";
import { Input } from "@/components/common/Input";

import { ClassesModalAdminView } from "./ClassesModalAdminView";
import { ClassesModalLecturerView } from "./ClassModalLecturerView";

import { useAuth } from "@/AuthProvider";

import { formatLecturerName, getNumOfStudents } from "@/utils/ClassUtils";

import {
  ColumnDef,
  ColumnFiltersState,
  Row,
  SortingState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
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
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  );

  const [openDialogRowId, setOpenDialogRowId] = useState<string | null>(null);
  const [selectedRow, setSelectedRow] = useState<IClass | null>(null);

  const { isAdmin, isLecturer } = useAuth();

  const handleRowClick = (row: Row<TData>) => {
    const id = (row.original as IClass).id.toString();

    setOpenDialogRowId(id);
    setSelectedRow(row.original as IClass);
  };

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onSortingChange: setSorting,
    getSortedRowModel: getSortedRowModel(),
    onColumnFiltersChange: setColumnFilters,
    getFilteredRowModel: getFilteredRowModel(),
    state: {
      sorting,
      columnFilters,
    },
  });

  return (
    <>
      <div className="flex items-center py-4">
        <Input
          placeholder="Search by class name..."
          value={(table.getColumn("name")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("name")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        />
      </div>
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
          {openDialogRowId !== null && selectedRow && isAdmin === true ? (
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
              accessToken={accessToken}
            />
          ) : null}
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 2xl:py-4">
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
