import React, { useEffect, useState } from "react";

import { Button } from "@/components/common/Button";
import { Input } from "@/components/common/Input";

import {
  ColumnDef,
  ColumnFiltersState,
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

import { exportToCSV } from "@/utils/Utils";

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  accessToken: string | null;
}

/**
 * Part of each data table class was taken from: https://ui.shadcn.com/docs/components/data-table
 */
export function ClassProfileDataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  );

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pages, setPages] = useState<number>(1);

  /**
   * Transforms the data array (TData) by deleting the id, so that the exported data
   * matches the visual table.
   * @returns A list of modified objects.
   */
  const preprocessData = () => {
    const preprocessedData = [];

    for (const studentProfileItem of data) {
      const processedStudent = {
        student_name: studentProfileItem.student_name,
        registration_number: studentProfileItem.reg_no,
        mark: studentProfileItem.mark,
        code: studentProfileItem.code,
      };

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
        pageSize: 9,
      },
    },
  });

  useEffect(() => {
    // https://stackoverflow.com/questions/36862334/get-viewport-window-height-in-reactjs
    const updateDataTablePageSize = () => {
      const TAILWIND_LG = 1024;
      const TAILWIND_XL = 1280;
      const TAILWIND_2_XL = 1536;

      const userScreenWidth = window.innerWidth;
      let pageSize = 9;

      if (userScreenWidth >= TAILWIND_2_XL) {
        pageSize = 9;
      } else if (userScreenWidth >= TAILWIND_XL) {
        pageSize = 6;
      } else if (userScreenWidth >= TAILWIND_LG) {
        pageSize = 5;
      }

      const newTotalPages = Math.ceil(data.length / pageSize);
      table.setPageSize(pageSize);
      setPages(newTotalPages);

      if (currentPage > newTotalPages) {
        setCurrentPage(newTotalPages);
      } else if (currentPage < 1) {
        setCurrentPage(1);
      }
    };

    updateDataTablePageSize();

    window.addEventListener("resize", updateDataTablePageSize);
    return () => window.removeEventListener("resize", updateDataTablePageSize);
  }, [table, data]);

  const handlePrev = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < pages) {
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <>
      <div className="flex flex-row justify-between py-2 w-full">
        <div className="flex items-center w-full">
          <Input
            placeholder="Search by student name..."
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
              "class-profiles"
            );
          }}
        >
          Export to CSV
        </Button>
      </div>
      <div className="rounded-md border w-full">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id} className="text-gray-800">
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
                  data-state={row.getIsSelected() && "selected"}
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
        </Table>
      </div>
      <div className="flex justify-between">
        <h2 className="2xl:text-sm xl:text-xs font-regular flex justify-self-end self-center pl-2 text-gray-600">
          {currentPage} of {pages} pages
        </h2>
        <div className="flex items-center justify-end space-x-2 2xl:py-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              table.previousPage();
              handlePrev();
            }}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              table.nextPage();
              handleNext();
            }}
            disabled={!table.getCanNextPage()}
          >
            Next
          </Button>
        </div>
      </div>
    </>
  );
}

export default ClassProfileDataTable;
