import React, { useState, useEffect } from "react";

import Papa from "papaparse";

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

import { generateCSVname } from "@/utils/Utils";

import { toast } from "sonner";

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

  const preprocessData = () => {
    const preprocessedData = [];

    for (const studentItem of data) {
      const processedStudent = {
        ...studentItem,
      };

      delete processedStudent.id;

      preprocessedData.push(processedStudent);
    }

    return preprocessedData;
  };

  const exportToCSV = () => {
    try {
      const dataToExport = preprocessData();
      const fileName = generateCSVname("students");

      if (dataToExport.length < 1) {
        toast.info("Nothing to export.");

        return;
      }

      const csv = Papa.unparse(dataToExport);

      const csvDataAsBlob = new Blob([csv], {
        type: "text/csv;charset=utf-8;",
      });

      const csvURL = window.URL.createObjectURL(csvDataAsBlob);
      const csvElement = document.createElement("a");

      csvElement.href = csvURL;
      csvElement.setAttribute("download", fileName);
      csvElement.click();

      toast.success("You have successfully exported this table to CSV!");
    } catch (error) {
      toast.error("Something went wrong when exporting this table to CSV.");
    }
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
            className="max-w-sm"
          />
        </div>
        <Button
          onClick={() => {
            exportToCSV();
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
