import { ColumnDef } from "@tanstack/react-table";

import { IMarkRow } from "../../../models/IMark";

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
];
