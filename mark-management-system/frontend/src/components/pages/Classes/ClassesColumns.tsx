import { ColumnDef } from "@tanstack/react-table";

import { IClass } from "@/models/IClass";
import { IMarkRow } from "@/models/IMark";

/**
 * Part of each column class was taken from: https://ui.shadcn.com/docs/components/data-table
 */
export const ClassColumns: ColumnDef<IClass>[] = [
  {
    accessorKey: "name",
    header: "Class Name",
  },
  {
    accessorKey: "code",
    header: "Class Code",
  },
  {
    accessorKey: "credit",
    header: "Class Credit",
  },
  {
    accessorKey: "credit_level",
    header: "Credit Level",
  },
  {
    accessorKey: "number_of_students",
    header: "Number of Students",
  },
  {
    accessorKey: "lecturer",
    header: "Lecturer",
  },
];

/**
 * Part of each column class was taken from: https://ui.shadcn.com/docs/components/data-table
 */
export const ClassProfileColumns: ColumnDef<IMarkRow>[] = [
  {
    accessorKey: "student_name",
    header: "Student Name",
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
];
