import axios from "axios";
import qs from "qs";

import { IUserLoginDetails, UserEdit } from "../models/IUser";

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
      .then((response) => {
        if (response.data) {
          localStorage.setItem("user", JSON.stringify(response.data));
        }
      })
      .catch((error) => {
        console.error(
          "Error: There has been an issue when authenticating.",
          error
        );
        throw error;
      });
  },

  getUsers: async (accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/users`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when fetching users.",
          error
        );
        throw error;
      });
  },

  getLecturers: async (accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/users/lecturers/`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when fetching lecturers.",
          error
        );
        throw error;
      });
  },

  editUser: async (userDetails: UserEdit, accessToken: string) => {
    return await axios
      .post(
        `${API_BASE_URL}/users/${userDetails.id}`,
        {
          id: userDetails.id,
          first_name: userDetails.first_name,
          last_name: userDetails.last_name,
          password: userDetails.password,
          confirm_password: userDetails.confirm_passsword,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      )
      .catch((error) => {
        console.error(
          "Error: There has been an issue when editing user details.",
          error
        );
        throw error;
      });
  },

  logout: async () => {
    localStorage.removeItem("user");
  },
};
