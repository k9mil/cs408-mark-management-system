import axios from "axios";

import { IMark } from "../models/IMark";

import { API_BASE_URL } from "../utils/Constants";

export const markService = {
  createMark: async (markDetails: IMark, accessToken: string) => {
    return await axios
      .post(
        `${API_BASE_URL}/marks`,
        {
          unique_code: markDetails.unique_code,
          mark: markDetails.mark,
          class_id: markDetails.class_id,
          student_id: markDetails.student_id,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      )
      .catch((error) => {
        console.error(
          "Error: There has been an issue when creating a mark.",
          error
        );
        throw error;
      });
  },

  getMark: async (uniqueCode: string, accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/marks/${uniqueCode}`, {
        data: { unique_code: uniqueCode },
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .catch((error) => {
        console.error(
          "Error: There has been an issue when retrieving a mark.",
          error
        );
        throw error;
      });
  },
};
