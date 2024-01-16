import { ColumnDef } from "@tanstack/react-table";

export type User = {
  id: number;
  first_name: string;
  last_name: string;
};

export type Class = {
  name: string;
  code: string;
  credit: number;
  credit_level: number;
  number_of_students: number;
  lecturer: User;
};

export const ClassColumns: ColumnDef<Class>[] = [
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
