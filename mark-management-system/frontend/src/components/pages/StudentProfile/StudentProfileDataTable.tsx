import React, { useEffect } from "react";

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

export function StudentProfileDataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  );

  /**
   * Transforms the data array (TData) by deleting the id, so that the exported data
   * matches the visual table.
   * @returns A list of modified objects.
   */
  const preprocessData = () => {
    const preprocessedData = [];

    for (const studentProfileItem of data) {
      const processedStudent = {
        ...studentProfileItem,
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
      const TAILWIND_LG = 1024;
      const TAILWIND_XL = 1280;
      const TAILWIND_2_XL = 1536;

      const userScreenWidth = window.innerWidth;

      if (userScreenWidth >= TAILWIND_2_XL) {
        table.setPageSize(10);
      } else if (userScreenWidth >= TAILWIND_XL) {
        table.setPageSize(6);
      } else if (userScreenWidth >= TAILWIND_LG) {
        table.setPageSize(5);
      }
    };

    updateDataTablePageSize();

    window.addEventListener("resize", updateDataTablePageSize);
    return () => window.removeEventListener("resize", updateDataTablePageSize);
  }, [table]);

  return (
    <>
      <div className="flex flex-row justify-between py-2 w-full">
        <div className="flex items-center w-full">
          <Input
            placeholder="Search by class code..."
            value={
              (table.getColumn("class_code")?.getFilterValue() as string) ?? ""
            }
            onChange={(event) =>
              table.getColumn("class_code")?.setFilterValue(event.target.value)
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
              "student-profiles"
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
      <div className="flex items-center justify-end space-x-2 2xl:py-4 w-full">
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

export default StudentProfileDataTable;
