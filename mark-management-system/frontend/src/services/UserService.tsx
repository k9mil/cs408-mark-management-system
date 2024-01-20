import axios from "axios";
import qs from "qs";

import { IUserLoginDetails } from "../models/IUser";

import { API_BASE_URL } from "../utils/Constants";

export const userService = {
  authenticateUser: async (userDetails: IUserLoginDetails) => {
    const stringifiedData = qs.stringify({
      username: userDetails.username,
      password: userDetails.password,
    });

    const headers = {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    };

    return await axios
      .post(`${API_BASE_URL}/users/login`, stringifiedData, headers)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when authenticating.",
          error
        );
        throw error;
      });
  },

  getUsers: async () => {
    return await axios
      .get(`${API_BASE_URL}/users`)
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when fetching lecturers.",
          error
        );
        throw error;
      });
  },
};
