import { ILecturer } from "@/models/IUser";

/**
 * Checks if a particular lecturer has uploaded marks for every one of their classes.
 * @param lecturer - The lecturer object.
 * @returns A string, "Yes" if uploaded for all classes, "No" otherwise. Also can return "N/A" if they don't teach any classes.
 */
export function uploadedForAllClasses(lecturer: ILecturer): string {
  if (lecturer && lecturer.classes.length === 0) {
    return "N/A";
  }

  return lecturer.classes.every((class_) => class_.is_uploaded) ? "Yes" : "No";
}
