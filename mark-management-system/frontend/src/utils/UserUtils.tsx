import { IUserEdit } from "@/models/IUser";

import { toast } from "sonner";

/**
 * Validates the user details, and ensures data integrity.
 * @param userDetails - The IUserEdit object containing the user details.
 * @returns A boolean, true if passes all validation or false if it fails at least one.
 */
export function validateUserEditDetails(userDetails: IUserEdit): boolean {
  if (!userDetails || typeof userDetails !== "object") {
    toast.error("Something went wrong. Please try again later.");
    return false;
  }

  if (userDetails.first_name === null || userDetails.first_name === "") {
    toast.error("First Name cannot be empty.");
    return false;
  }

  if (userDetails.last_name === null || userDetails.last_name === "") {
    toast.error("Last Name cannot be empty.");
    return false;
  }

  if (userDetails.password && !userDetails.confirm_passsword) {
    toast.error("You must confirm your password.");
    return false;
  }

  if (
    userDetails.password &&
    userDetails.confirm_passsword &&
    userDetails.password !== userDetails.confirm_passsword
  ) {
    toast.error("The passwords do not match.");
    return false;
  }

  return true;
}
