import { IMarkEdit } from "@/models/IMark";

import { isNumber } from "./Utils";

import { toast } from "sonner";

export function validateMarkDetailsOnEdit(markDetails: IMarkEdit) {
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

  if (!("unique_code" in markDetails) || markDetails.unique_code === null) {
    toast.error("The Unique Code is missing.");
    return false;
  }

  return true;
}
