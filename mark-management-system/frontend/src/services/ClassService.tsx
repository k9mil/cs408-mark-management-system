import axios from "axios";

import { API_BASE_URL } from "../utils/constants";

export const classService = {
  getClasses: async () => {
    return await axios
      .get(`${API_BASE_URL}/classes`)
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when fetching classes.",
          error
        );
        throw error;
      });
  },
};
