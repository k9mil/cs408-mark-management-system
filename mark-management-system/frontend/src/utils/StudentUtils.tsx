import { IMarkEdit } from "@/models/IMark";

import { isNumber } from "./Utils";

import { toast } from "sonner";

/**
 * Validates the mark details, and ensures data integrity.
 * @param markDetails - The IMarkEdit object containing the mark details.
 * @returns A boolean, true if passes all validation or false if it fails at least one.
 */
export function validateMarkDetailsOnEdit(markDetails: IMarkEdit): boolean {
  if (!markDetails || typeof markDetails !== "object") {
    toast.error("Something went wrong. Please try again later.");
    return false;
  }

  if (!("mark" in markDetails) || markDetails.mark === null) {
    toast.error("Mark is missing.");
    return false;
  }

  if (!isNumber(markDetails.mark)) {
    toast.error("Mark should be an integer.");
    return false;
  }

  if (markDetails.mark < 0 || markDetails.mark > 100) {
    toast.error("Mark should be between 0 and 100.");
    return false;
  }

  return true;
}
