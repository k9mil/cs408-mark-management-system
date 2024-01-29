import { ILecturer } from "@/models/IUser";

export function uploadedForAllClasses(lecturer: ILecturer): string {
  if (lecturer && lecturer.classes.length === 0) {
    return "N/A";
  }

  return lecturer.classes.every((class_) => class_.is_uploaded) ? "Yes" : "No";
}
