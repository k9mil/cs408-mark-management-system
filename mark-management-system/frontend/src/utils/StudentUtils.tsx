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

  if ("mark" in markDetails && markDetails.mark !== null) {
    if (!isNumber(markDetails.mark)) {
      toast.error(`Mark should be an integer.`);
      return false;
    }

    if (markDetails.mark < 0 || markDetails.mark > 100) {
      toast.error(`Mark should be between 0 and 100.`);
      return false;
    }

    if (markDetails.code) {
      if (
        markDetails.code !== "EX" &&
        markDetails.code !== "FO" &&
        markDetails.code !== "IA" &&
        markDetails.code !== "PM"
      ) {
        toast.error(
          `An invalid mark code has been provided. The options are: EX, FO, IA, PM`
        );
        return false;
      }
    }
  } else {
    if (
      !markDetails.code ||
      (markDetails.code !== "ABS" &&
        markDetails.code !== "EN" &&
        markDetails.code !== "UM")
    ) {
      toast.error(
        `A valid mark code is required if no mark is provided. The options are: ABS, EN, UM`
      );
      return false;
    }
  }

  return true;
}
