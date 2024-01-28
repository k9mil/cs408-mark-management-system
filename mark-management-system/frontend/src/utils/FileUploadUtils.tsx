import { IMarkRow } from "@/models/IMark";

import { toast } from "sonner";

import { isValidClassCode } from "./ClassUtils";
import { isNumber } from "./Utils";

export function validateParsedFile(fileContents: IMarkRow[] | null) {
  if (!fileContents || !Array.isArray(fileContents)) {
    toast.error("The file provided is empty or corrupt.");
    return false;
  }

  for (let i = 0; i < fileContents.length; i++) {
    const row = fileContents[i];

    if (Object.keys(row).length != 7) {
      toast.error(
        `Row ${i + 1} doesn't contain all necessary information. 
        The row should have the following: 
        CLASS_CODE, REG_NO, MARK, STUDENT_NAME, DEGREE_LEVEL, DEGRE_NAME, UNIQUE_CODE`
      );

      return false;
    }

    if (!("CLASS_CODE" in row) || row.CLASS_CODE === null) {
      toast.error(
        `Row ${
          i + 1
        } doesn't contain a class code. Please fix the file and try again.`
      );
      return false;
    }

    if (!isValidClassCode(row.CLASS_CODE)) {
      toast.error(
        `Row ${i + 1} should have a Class code in the format of: "AB123"`
      );

      return false;
    }

    if (!("REG_NO" in row) || row.REG_NO === null) {
      toast.error(
        `Row ${
          i + 1
        } doesn't contain a registration number. Please fix the file and try again.`
      );
      return false;
    }

    if (!("MARK" in row) || row.MARK === null) {
      toast.error(
        `Row ${
          i + 1
        } doesn't contain a mark. Please fix the file and try again.`
      );
      return false;
    }

    if (!isNumber(row.MARK)) {
      toast.error(`Row ${i + 1} should have a mark which is an integer.`);
      return false;
    }

    if (row.MARK < 0 || row.MARK > 100) {
      toast.error(`Row ${i + 1} should have a mark between 0 and 100.`);

      return false;
    }

    if (!("STUDENT_NAME" in row) || row.STUDENT_NAME === null) {
      toast.error(
        `Row ${
          i + 1
        } doesn't contain a student name. Please fix the file and try again.`
      );
      return false;
    }

    if (!("DEGREE_LEVEL" in row) || row.DEGREE_LEVEL === null) {
      toast.error(
        `Row ${
          i + 1
        } doesn't contain a degree level. Please fix the file and try again.`
      );
      return false;
    }

    // TODO: Add validation for the "Undergradute Board", i.e. titles like BSc

    if (!("DEGREE_NAME" in row) || row.DEGREE_NAME === null) {
      toast.error(
        `Row ${
          i + 1
        } doesn't contain a degree name. Please fix the file and try again.`
      );
      return false;
    }

    if (!("UNIQUE_CODE" in row) || row.UNIQUE_CODE === null) {
      toast.error(
        `Row ${
          i + 1
        } doesn't contain a unique code. Please fix the file and try again.`
      );
      return false;
    }
  }

  return true;
}
