import { toast } from "sonner";

import { isNumber } from "./Utils";

import { IClassWithId, IClassWithLecturerId } from "@/models/IClass";
import { IUser } from "@/models/IUser";
import { IStudent } from "@/models/IStudent";

/**
 * Checks if a class code is valid, i.e. if it's two upper case letters followed bythree digits.
 * @param input - The class code which will get validated.
 * @returns A boolean, true if valid else false.
 */
export function isValidClassCode(input: string): boolean {
  const pattern = /^[A-Z]{2}\d{3}$/;

  return pattern.test(input);
}

/**
 * Formats the lecturer name in the format of "FirstName LastName" given an IUser object.
 * @param lecturer - The lecturer object containing the first name & last name.
 * @returns The formatted string.
 */
export function formatLecturerName(lecturer: IUser): string {
  return `${lecturer.first_name} ${lecturer.last_name}`;
}

/**
 * Returns the number of students in a student array.
 * @param students - The student array of IStudent objects.
 * @returns A number, the length of the array.
 */
export function getNumOfStudents(students: IStudent[]): number {
  if (students.length !== 0) return students.length;
  return 0;
}

/**
 * Validates the class details, and ensures data integrity.
 * @param classDetails - The classDetails, which can either be in the form of a "IClassWithId"
 *                       object when the class is being edited, or "IClassWithLecturerId" when it's being created.
 * @returns A boolean, true if passes all validation or false if it fails at least one.
 */
export function validateClassDetails(
  classDetails: IClassWithId | IClassWithLecturerId
) {
  if (!classDetails || typeof classDetails !== "object") {
    toast.error("Something went wrong. Please try again later.");
    return false;
  }

  if (
    !("name" in classDetails) ||
    classDetails.name === null ||
    classDetails.name === ""
  ) {
    toast.error("Name is missing.");
    return false;
  }

  if (
    !("code" in classDetails) ||
    classDetails.code === null ||
    classDetails.code === ""
  ) {
    toast.error("Class Code is missing.");
    return false;
  }

  if (!("credit" in classDetails) || classDetails.credit === null) {
    toast.error("Class Credits are missing.");
    return false;
  }

  if (!("credit_level" in classDetails) || classDetails.credit_level === null) {
    toast.error("Class Credit Level is missing.");
    return false;
  }

  if (!("lecturer_id" in classDetails) || classDetails.lecturer_id === null) {
    toast.error("A lecturer has to be assigned.");
    return false;
  }

  if (!isNumber(classDetails.credit)) {
    toast.error("Credit should be an integer!");
    return false;
  }

  if (!isNumber(classDetails.credit_level)) {
    toast.error("Credit Level should be an integer!");
    return false;
  }

  if (!isValidClassCode(classDetails.code)) {
    toast.error("Class code should be in the format of: `AB123`");
    return false;
  }

  if (
    classDetails.credit !== 10 &&
    classDetails.credit !== 20 &&
    classDetails.credit !== 40 &&
    classDetails.credit !== 80
  ) {
    toast.error("Class Credit should be: 10, 20, 40 or 80.");
    return false;
  }

  if (classDetails.credit_level < 1 || classDetails.credit_level > 5) {
    toast.error("Credit Level should be between 1 and 5.");
    return false;
  }

  return true;
}
