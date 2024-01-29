import { ColumnDef } from "@tanstack/react-table";

import { ILecturer } from "@/models/IUser";

export const LecturerColumns: ColumnDef<ILecturer>[] = [
  {
    accessorKey: "firstName",
    header: "First Name",
  },
  {
    accessorKey: "lastName",
    header: "Last Name",
  },
  {
    accessorKey: "numberOfClasses",
    header: "Number of Classes Taught",
  },
  {
    accessorKey: "uploadedForAllClasses",
    header: "Uploaded for all Classes",
  },
];
