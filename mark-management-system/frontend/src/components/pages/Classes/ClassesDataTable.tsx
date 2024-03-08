import React, { useState, useEffect } from "react";

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

import { exportToCSV } from "@/utils/Utils";

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

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pages, setPages] = useState<number>(1);

  const { isAdmin, isLecturer } = useAuth();

  const handleRowClick = (row: Row<TData>) => {
    const id = (row.original as IClass).id.toString();

    setOpenDialogRowId(id);
    setSelectedRow(row.original as IClass);
  };

  /**
   * Transforms the data array (TData) by adding the number_of_students and lecturer, so that the exported data
   * matches the visual table.
   * @returns A list of modified objects.
   */
  const preprocessData = () => {
    const preprocessedData = [];

    for (const classItem of data) {
      const processedClass = {
        ...classItem,
        lecturer: formatLecturerName((classItem as IClass).lecturer),
        number_of_students: getNumOfStudents((classItem as IClass).students),
      };

      delete processedClass.id;
      delete processedClass.students;
      delete processedClass.marks;

      preprocessedData.push(processedClass);
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
      let pageSize = 10;

      if (userScreenWidth >= TAILWIND_2_XL) {
        pageSize = 10;
      } else if (userScreenWidth >= TAILWIND_XL) {
        pageSize = 8;
      } else if (userScreenWidth >= TAILWIND_LG) {
        pageSize = 7;
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
      <div className="flex flex-row justify-between py-2">
        <div className="flex items-center w-full">
          <Input
            placeholder="Search by class code..."
            value={(table.getColumn("code")?.getFilterValue() as string) ?? ""}
            onChange={(event) =>
              table.getColumn("code")?.setFilterValue(event.target.value)
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
              "classes"
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

export default ClassesDataTable;
