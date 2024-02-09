import { IMarkRow } from "@/models/IMark";

import { toast } from "sonner";

import { isValidClassCode } from "./ClassUtils";
import { isNumber } from "./Utils";

/**
 * Validates the parsed file (uploaded marks), and ensures data integrity.
 * @param fileContents - A list of IMarkRow objects, or null.
 * @returns A boolean, true if passes all validation or false if it fails at least one.
 */
export function validateParsedFile(fileContents: IMarkRow[] | null): boolean {
  if (!fileContents || !Array.isArray(fileContents)) {
    toast.error("The file provided is empty or corrupt.");
    return false;
  }

  const firstClassCode = fileContents[0].class_code;

  for (let i = 0; i < fileContents.length; i++) {
    const row = fileContents[i];

    if (Object.keys(row).length != 7) {
      toast.error(
        `Row ${i + 2} doesn't contain all necessary information. 
        The row should have the following: 
        CLASS_CODE, REG_NO, MARK, STUDENT_NAME, DEGREE_LEVEL, DEGREE_NAME, UNIQUE_CODE`
      );

      return false;
    }

    if (row.class_code !== firstClassCode) {
      toast.error(
        `Row ${
          i + 2
        } has a different class code to previous rows. Please fix the file and try again.`
      );
      return false;
    }

    if (!("class_code" in row) || row.class_code === null) {
      toast.error(
        `Row ${
          i + 2
        } doesn't contain a class code. Please fix the file and try again.`
      );
      return false;
    }

    if (!isValidClassCode(row.class_code)) {
      toast.error(
        `Row ${i + 2} should have a Class code in the format of: "AB123"`
      );

      return false;
    }

    if (!("reg_no" in row) || row.reg_no === null) {
      toast.error(
        `Row ${
          i + 2
        } doesn't contain a registration number. Please fix the file and try again.`
      );
      return false;
    }

    if (!("mark" in row) || row.mark === null) {
      toast.error(
        `Row ${
          i + 2
        } doesn't contain a mark. Please fix the file and try again.`
      );
      return false;
    }

    if (!isNumber(row.mark)) {
      toast.error(`Row ${i + 2} should have a mark which is an integer.`);
      return false;
    }

    if (row.mark < 0 || row.mark > 100) {
      toast.error(`Row ${i + 2} should have a mark between 0 and 100.`);

      return false;
    }

    if (!("student_name" in row) || row.student_name === null) {
      toast.error(
        `Row ${
          i + 2
        } doesn't contain a student name. Please fix the file and try again.`
      );
      return false;
    }

    if (!("degree_level" in row) || row.degree_level === null) {
      toast.error(
        `Row ${
          i + 2
        } doesn't contain a degree level. Please fix the file and try again.`
      );
      return false;
    }

    // TODO: Add validation for the "Undergradute Board", i.e. titles like BSc

    if (!("degree_name" in row) || row.degree_name === null) {
      toast.error(
        `Row ${
          i + 2
        } doesn't contain a degree name. Please fix the file and try again.`
      );
      return false;
    }

    if (!("unique_code" in row) || row.unique_code === null) {
      toast.error(
        `Row ${
          i + 2
        } doesn't contain a unique code. Please fix the file and try again.`
      );
      return false;
    }
  }

  return true;
}
