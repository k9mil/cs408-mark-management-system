import { toast } from "sonner";

import { IUser } from "../models/IUser";
import { IClassWithId, IClassWithLecturerId } from "../models/IClass";

import { isNumber } from "./Utils";

export function formatLecturerName(lecturer: IUser) {
  return `${lecturer.first_name} ${lecturer.last_name}`;
}

export function getNumOfStudents(students: Array<IUser>) {
  if (students) return students.length;
  return 0;
}

export function validateClassDetails(
  classDetails: IClassWithId | IClassWithLecturerId
) {
  if (!isNumber(classDetails.credit)) {
    toast.error("Credit should be an integer!");
    return false;
  }

  if (!isNumber(classDetails.credit_level)) {
    toast.error("Credit Level should be an integer!");
    return false;
  }

  return true;
}
