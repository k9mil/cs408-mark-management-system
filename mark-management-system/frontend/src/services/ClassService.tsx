import axios from "axios";

import { ClassDTO } from "../components/pages/Classes/ClassesColumns";

import { API_BASE_URL } from "../utils/constants";

export const classService = {
  createClass: async (classDetails: ClassDTO) => {
    return await axios
      .post(`${API_BASE_URL}/classes`, {
        name: classDetails.name,
        code: classDetails.code,
        credit: classDetails.credit,
        credit_level: classDetails.credit_level,
        lecturer_id: classDetails.lecturer_id,
      })
      .catch((error) => {
        console.error(
          "Error: There has been an issue when creating a class.",
          error
        );
        throw error;
      });
  },

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
