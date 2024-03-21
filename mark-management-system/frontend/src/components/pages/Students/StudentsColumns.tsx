import { ColumnDef } from "@tanstack/react-table";

import { IMarkRow } from "../../../models/IMark";

/**
 * Part of each column class was taken from: https://ui.shadcn.com/docs/components/data-table
 */
export const StudentColumns: ColumnDef<IMarkRow>[] = [
  {
    accessorKey: "class_code",
    header: "Class Code",
  },
  {
    accessorKey: "reg_no",
    header: "Registration Number",
  },
  {
    accessorKey: "mark",
    header: "Mark",
  },
  {
    accessorKey: "code",
    header: "Mark Code",
  },
  {
    accessorKey: "student_name",
    header: "Student Name",
  },
  {
    accessorKey: "degree_level",
    header: "Degree Level",
  },
  {
    accessorKey: "degree_name",
    header: "Degree Name",
  },
];

/**
 * Part of each column class was taken from: https://ui.shadcn.com/docs/components/data-table
 */
export const StudentProfileColumns: ColumnDef<IMarkRow>[] = [
  {
    accessorKey: "class_code",
    header: "Class Code",
  },
  {
    accessorKey: "class_name",
    header: "Class Name",
  },
  {
    accessorKey: "mark",
    header: "Mark",
  },
  {
    accessorKey: "code",
    header: "Mark Code",
  },
];
