import { IUser } from "../models/IUser";

export function formatLecturerName(lecturer: IUser) {
  return `${lecturer.first_name} ${lecturer.last_name}`;
}

export function getNumOfStudents(students: Array<IUser>) {
  if (students) return students.length;
  return 0;
}
