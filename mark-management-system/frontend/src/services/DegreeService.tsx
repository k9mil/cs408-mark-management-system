import axios from "axios";

import { IDegree } from "../models/IDegree";

import { API_BASE_URL } from "../utils/Constants";

export const degreeService = {
  createDegree: async (degreeDetails: IDegree, accessToken: string) => {
    return await axios
      .post(
        `${API_BASE_URL}/classes`,
        {
          name: degreeDetails.name,
          level: degreeDetails.level,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      )
      .catch((error) => {
        console.error(
          "Error: There has been an issue when creating a degree.",
          error
        );
        throw error;
      });
  },

  getDegree: async (degreeName: string, accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/degrees/${degreeName}`, {
        data: { degree_name: degreeName },
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .catch((error) => {
        console.error(
          "Error: There has been an issue when retrieving a degree.",
          error
        );
        throw error;
      });
  },
};
