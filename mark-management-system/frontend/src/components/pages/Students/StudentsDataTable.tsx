import React, { useState, useEffect } from "react";

import { Button } from "@/components/common/Button";
import { Input } from "@/components/common/Input";

import { StudentsModal } from "./StudentsModal";

import { useAuth } from "@/AuthProvider";

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

import { IMarkRow } from "@/models/IMark";

import { exportToCSV } from "@/utils/Utils";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  accessToken: string | null;
  marksData: () => Promise<void>;
}

export function StudentsDataTable<TData, TValue>({
  columns,
  data,
  accessToken,
  marksData,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  );

  const [openDialogRowId, setOpenDialogRowId] = useState<string | null>(null);
  const [selectedRow, setSelectedRow] = useState<IMarkRow | null>(null);

  const { isLecturer } = useAuth();

  const handleRowClick = (row: Row<TData>) => {
    const id = (row.original as IMarkRow).id.toString();

    setOpenDialogRowId(id);
    setSelectedRow(row.original as IMarkRow);
  };

  /**
   * Transforms the data array (TData) by deleting the id, so that the exported data
   * matches the visual table.
   * @returns A list of modified objects.
   */
  const preprocessData = () => {
    const preprocessedData = [];

    for (const studentItem of data) {
      const processedStudent = {
        ...studentItem,
      };

      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      delete processedStudent.id;

      preprocessedData.push(processedStudent);
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
    initialState: {
      pagination: {
        pageSize: 10,
      },
    },
  });

  useEffect(() => {
    // https://stackoverflow.com/questions/36862334/get-viewport-window-height-in-reactjs
    const updateDataTablePageSize = () => {
      const TAILWIND_XL = 1280;
      const TAILWIND_2_XL = 1536;

      const userScreenWidth = window.innerWidth;

      if (userScreenWidth >= TAILWIND_2_XL) {
        table.setPageSize(10);
      } else if (userScreenWidth >= TAILWIND_XL) {
        table.setPageSize(8);
      }
    };

    updateDataTablePageSize();

    window.addEventListener("resize", updateDataTablePageSize);
    return () => window.removeEventListener("resize", updateDataTablePageSize);
  }, [table]);

  return (
    <>
      <div className="flex flex-row justify-between py-2">
        <div className="flex items-center w-full">
          <Input
            placeholder="Search by name..."
            value={
              (table.getColumn("student_name")?.getFilterValue() as string) ??
              ""
            }
            onChange={(event) =>
              table
                .getColumn("student_name")
                ?.setFilterValue(event.target.value)
            }
            className="max-w-[15rem]"
          />
        </div>
        <Button
          onClick={() => {
            const convertedObjects = preprocessData();

            exportToCSV(
              convertedObjects,
              "You have successfully exported this table to CSV.",
              "students"
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
                      {flexRender(
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
          {openDialogRowId !== null && selectedRow && isLecturer === true ? (
            <StudentsModal
              row={selectedRow}
              openDialogRowId={openDialogRowId}
              setOpenDialogRowId={setOpenDialogRowId}
              accessToken={accessToken}
              marksData={marksData}
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

export default StudentsDataTable;
