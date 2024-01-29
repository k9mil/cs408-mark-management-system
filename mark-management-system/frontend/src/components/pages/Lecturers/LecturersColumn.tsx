import { ColumnDef } from "@tanstack/react-table";

import { IClass } from "../../../models/IClass";

export const LecturerColumns: ColumnDef<IClass>[] = [
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
