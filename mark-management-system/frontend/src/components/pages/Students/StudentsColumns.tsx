import { ColumnDef } from "@tanstack/react-table";

export type Student = {
  class_code: string;
  registration_number: string;
  mark: number;
  student_name: string;
  degree_level: string;
  degree: string;
};

export const StudentColumns: ColumnDef<Student>[] = [
  {
    accessorKey: "class_code",
    header: "Class Code",
  },
  {
    accessorKey: "registration_number",
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
    accessorKey: "degree",
    header: "Degree",
  },
];
