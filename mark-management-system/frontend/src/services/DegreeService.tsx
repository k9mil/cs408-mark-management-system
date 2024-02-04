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

  getDegrees: async (degreeSet: Set<string>, accessToken: string) => {
    const degrees = Array.from(degreeSet).map((degree) => JSON.parse(degree));

    return await axios
      .post(`${API_BASE_URL}/degrees/search/`, degrees, {
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
