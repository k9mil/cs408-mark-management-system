import axios from "axios";

import { API_BASE_URL } from "../utils/constants";

export const userService = {
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
