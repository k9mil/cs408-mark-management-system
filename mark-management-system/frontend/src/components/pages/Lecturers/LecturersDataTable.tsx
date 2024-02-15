import React, { useState } from "react";

import { Button } from "@/components/common/Button";
import { Input } from "@/components/common/Input";

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

import { uploadedForAllClasses } from "@/utils/LecturerUtils";
import { ILecturer } from "@/models/IUser";

import LecturersModalView from "./LecturersModalView";

import { exportToCSV } from "@/utils/Utils";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

export function LecturersDataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  );

  const [openDialogRowId, setOpenDialogRowId] = useState<string | null>(null);
  const [selectedRow, setSelectedRow] = useState<ILecturer | null>(null);

  const handleRowClick = (row: Row<TData>) => {
    const id = (row.original as ILecturer).id.toString();

    setOpenDialogRowId(id);
    setSelectedRow(row.original as ILecturer);
  };

  const preprocessData = () => {
    const preprocessedData = [];

    for (const lecturerItem of data) {
      const processedLecturer = {
        ...lecturerItem,
        uploaded_for_all_classes: uploadedForAllClasses(
          lecturerItem as ILecturer
        ),
      };

      delete processedLecturer.id;
      delete processedLecturer.classes;

      preprocessedData.push(processedLecturer);
    }

    return preprocessedData;
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
      <div className="flex flex-row justify-between py-2">
        <div className="flex items-center">
          <Input
            placeholder="Search by last name..."
            value={
              (table.getColumn("last_name")?.getFilterValue() as string) ?? ""
            }
            onChange={(event) =>
              table.getColumn("last_name")?.setFilterValue(event.target.value)
            }
            className="max-w-sm"
          />
        </div>
        <Button
          onClick={() => {
            const convertedObjects = preprocessData();

            exportToCSV(
              convertedObjects,
              "You have successfully exported this table to CSV.",
              "lecturers"
            );
          }}
        >
          Export to CSV
        </Button>
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
                      {cell.column.id === "uploaded_for_all_classes"
                        ? (() => {
                            const isUploadedForAllClasses =
                              uploadedForAllClasses(
                                cell.row.original as ILecturer
                              );
                            const textColorClass =
                              isUploadedForAllClasses === "Yes"
                                ? "text-green-500 font-bold"
                                : isUploadedForAllClasses === "No"
                                ? "text-red-500 font-bold"
                                : "font-base";
                            return (
                              <span className={textColorClass}>
                                {isUploadedForAllClasses}
                              </span>
                            );
                          })()
                        : flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                    </TableCell>
                  ))}
                </TableRow>
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
          {openDialogRowId !== null && selectedRow ? (
            <LecturersModalView
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

export default LecturersDataTable;
