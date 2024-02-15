import { IMarkRow, IMarkMyPlace } from "@/models/IMark";

import { toast } from "sonner";

import { isValidClassCode } from "./ClassUtils";
import { isNumber } from "./Utils";

/**
 * Validates the parsed file (uploaded marks), and ensures data integrity.
 * @param fileContents - A list of IMarkRow objects, or null.
 * @returns A boolean, true if passes all validation or false if it fails at least one.
 */
export function validateUploadFile(fileContents: IMarkRow[] | null): boolean {
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

/**
 * Validates the parsed file (for the conversion between MyPlace to MMS), and ensures data integrity.
 * @param fileContents - A list of IMarkMyPlace objects, or null.
 * @returns A boolean, true if passes all validation or false if it fails at least one.
 */
export function validateMyPlaceFile(
  fileContents: IMarkMyPlace[] | null
): boolean {
  if (!fileContents || !Array.isArray(fileContents)) {
    toast.error("The file provided is empty or corrupt.");
    return false;
  }

  const firstClassCode = fileContents[0].class_code;

  for (let i = 0; i < fileContents.length; i++) {
    const row = fileContents[i];

    if (Object.keys(row).length != 5) {
      toast.error(
        `Row ${i + 2} doesn't contain all necessary information. 
        The row should have the following: 
        CLASS_CODE, DATE, REG_NO, CLASS_TOTAL, OVERRIDE_MARK`
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

    if (!("date" in row) || row.date === null) {
      toast.error(
        `Row ${
          i + 2
        } doesn't contain a date. Please fix the file and try again.`
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

    if (!("class_total" in row) || row.class_total === null) {
      toast.error(
        `Row ${
          i + 2
        } doesn't contain a class total. Please fix the file and try again.`
      );
      return false;
    }

    if (!("override_mark" in row) || row.override_mark === null) {
      toast.error(
        `Row ${
          i + 2
        } doesn't contain an override mark. Please fix the file and try again.`
      );
      return false;
    }

    if (!isNumber(row.class_total)) {
      toast.error(
        `Row ${i + 2} should have a class total which is an integer.`
      );
      return false;
    }

    if (row.class_total < 0 || row.class_total > 100) {
      toast.error(`Row ${i + 2} should have a class total between 0 and 100.`);

      return false;
    }

    if (!isNumber(row.override_mark)) {
      toast.error(
        `Row ${i + 2} should have an override mark which is an integer.`
      );
      return false;
    }

    if (row.override_mark < 0 || row.override_mark > 100) {
      toast.error(
        `Row ${i + 2} should have an override mark between 0 and 100.`
      );

      return false;
    }
  }

  return true;
}
