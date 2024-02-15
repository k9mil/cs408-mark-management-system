import { IMarkRow, IMarkMyPlace } from "@/models/IMark";

import Papa from "papaparse";

import { toast } from "sonner";

// https://stackoverflow.com/questions/23437476/in-typescript-how-to-check-if-a-string-is-numeric
export const isNumber = (value?: string | number): boolean => {
  return value != null && value !== "" && !isNaN(Number(value.toString()));
};

// https://stackoverflow.com/questions/12539574/whats-the-best-way-most-efficient-to-turn-all-the-keys-of-an-object-to-lower
export const toLowerCaseIMarkRow = (fileContents: IMarkRow[]): IMarkRow[] => {
  return fileContents.map(
    (obj: IMarkRow) =>
      Object.fromEntries(
        Object.entries(obj).map(([key, value]) => [key.toLowerCase(), value])
      ) as IMarkRow
  );
};

// https://stackoverflow.com/questions/12539574/whats-the-best-way-most-efficient-to-turn-all-the-keys-of-an-object-to-lower
export const toLowerCaseIMarkMyPlace = (
  fileContents: IMarkMyPlace[]
): IMarkMyPlace[] => {
  return fileContents.map(
    (obj: IMarkMyPlace) =>
      Object.fromEntries(
        Object.entries(obj).map(([key, value]) => [key.toLowerCase(), value])
      ) as IMarkMyPlace
  );
};

export const generateCSVname = (page: string): string => {
  const date = new Date();

  return `mark_management_system_${page}_${date.toISOString()}.csv`;
};

export const exportToCSV = (
  dataToExport: any,
  successMessage: string,
  entityName: string
) => {
  try {
    const fileName = generateCSVname(entityName);

    if (dataToExport.length < 1) {
      toast.info("Nothing to export.");
      return;
    }

    const csv = Papa.unparse(dataToExport);
    const csvDataAsBlob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const csvURL = window.URL.createObjectURL(csvDataAsBlob);
    const csvElement = document.createElement("a");

    csvElement.href = csvURL;
    csvElement.setAttribute("download", fileName);
    csvElement.click();

    toast.success(successMessage);
  } catch (error) {
    toast.error("Something went wrong when exporting to CSV.");
  }
};
