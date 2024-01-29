import { ILecturer } from "@/models/IUser";

export function uploadedForAllClasses(lecturer: ILecturer): string {
  return lecturer.classes.every((class_) => class_.is_uploaded) ? "Yes" : "No";
}
