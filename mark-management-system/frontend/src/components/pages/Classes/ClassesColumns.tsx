import { ColumnDef } from "@tanstack/react-table";

import { IClass } from "@/models/IClass";
import { IMarkRow } from "@/models/IMark";

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

export const ClassProfileColumns: ColumnDef<IMarkRow>[] = [
  {
    accessorKey: "class_code",
    header: "Class Code",
  },
  {
    accessorKey: "class_name",
    header: "Class Name",
  },
  {
    accessorKey: "student_name",
    header: "Student Name",
  },
  {
    accessorKey: "mark",
    header: "Mark",
  },
];
