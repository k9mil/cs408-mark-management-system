import axios from "axios";

import { IPersonalCircumstance } from "../models/IPersonalCircumstance";

import { API_BASE_URL } from "../utils/Constants";

export const personalCircumstanceService = {
  createPersonalCircumstance: async (
    personalCircumstanceDetails: IPersonalCircumstance,
    accessToken: string
  ) => {
    return await axios
      .post(
        `${API_BASE_URL}/personal-circumstances/`,
        {
          reg_no: personalCircumstanceDetails.reg_no,
          details: personalCircumstanceDetails.details,
          semester: personalCircumstanceDetails.semester,
          cat: personalCircumstanceDetails.cat,
          comments: personalCircumstanceDetails.comments,
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

  getPersonalCircumstancesForStudent: async (
    regNo: string,
    accessToken: string
  ) => {
    return await axios
      .get(`${API_BASE_URL}/personal-circumstances/${regNo}`, {
        data: { reg_no: regNo },
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when retrieving personal circumstances for a student.",
          error
        );
        throw error;
      });
  },
};
