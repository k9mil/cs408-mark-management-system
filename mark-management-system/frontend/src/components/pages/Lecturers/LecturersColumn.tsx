import { ColumnDef } from "@tanstack/react-table";

import { ILecturer } from "@/models/IUser";

/**
 * Part of each column class was taken from: https://ui.shadcn.com/docs/components/data-table
 */
export const LecturerColumns: ColumnDef<ILecturer>[] = [
  {
    accessorKey: "first_name",
    header: "First Name",
  },
  {
    accessorKey: "last_name",
    header: "Last Name",
  },
  {
    accessorKey: "number_of_classes_taught",
    header: "Number of Classes taught",
  },
  {
    accessorKey: "uploaded_for_all_classes",
    header: "Uploaded for all Classes",
  },
];
