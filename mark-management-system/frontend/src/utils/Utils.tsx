import { IMarkRow, IMarkMyPlace } from "@/models/IMark";
import { IPersonalCircumstanceRow } from "@/models/IPersonalCircumstance";

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

// https://stackoverflow.com/questions/12539574/whats-the-best-way-most-efficient-to-turn-all-the-keys-of-an-object-to-lower
export const toLowerCaseIPersonalCircumstanceRow = (
  fileContents: IPersonalCircumstanceRow[]
): IPersonalCircumstanceRow[] => {
  return fileContents.map(
    (obj: IPersonalCircumstanceRow) =>
      Object.fromEntries(
        Object.entries(obj).map(([key, value]) => [key.toLowerCase(), value])
      ) as IPersonalCircumstanceRow
  );
};

/**
 * Generates a CSV name to be used for the exported csv.
 * @param text - The custom text which tells the user which file was downloaded.
 * @returns A string containing the generated file name.
 */
export const generateCSVname = (text: string): string => {
  const date = new Date();

  return `mark_management_system_${text}_${date.toISOString()}.csv`;
};

/**
 * Exports & triggers a download of the CSV to the user's machine.
 * @param dataToExport - The data to be exported, i.e contained within the downloaded CSV.
 * @param successMessage - A custom success message if no errors happen during the exporting process.
 * @param text - Custom text which modifies the name of the generated CSV file.
 * @returns - N/A, an empty return if length of data < 1
 */
export const exportToCSV = (
  dataToExport: any,
  successMessage: string,
  text: string
) => {
  try {
    const fileName = generateCSVname(text);

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
