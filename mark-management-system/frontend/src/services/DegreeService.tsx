import axios from "axios";
import qs from "qs";

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
      .then((response) => {
        return { data: response.data, statusCode: response.status };
      })
      .catch((error) => {
        return {
          data: error.response.data.detail,
          statusCode: error.response.status,
        };
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
      .then((response) => {
        return { data: response.data, statusCode: response.status };
      })
      .catch((error) => {
        return {
          data: error.response.data.detail,
          statusCode: error.response.status,
        };
      });
  },

  getDegrees: async (degreeNames: Set<string>, accessToken: string) => {
    const queryString = qs.stringify(
      { degree_names: Array.from(degreeNames) },
      { arrayFormat: "repeat" }
    );

    return await axios
      .get(`${API_BASE_URL}/degrees/?${queryString}`, {
        data: { degree_names: degreeNames },
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => {
        return { data: response.data, statusCode: response.status };
      })
      .catch((error) => {
        return {
          data: error.response.data.detail,
          statusCode: error.response.status,
        };
      });
  },
};
