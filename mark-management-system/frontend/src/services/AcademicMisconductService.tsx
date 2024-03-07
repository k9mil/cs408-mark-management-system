import axios from "axios";

import { API_BASE_URL } from "../utils/Constants";

import { IAcademicMisconduct } from "@/models/IAcademicMisconduct";

export const academicMisconductService = {
  createAcademicMisconduct: async (
    academicMisconductDetails: IAcademicMisconduct,
    accessToken: string
  ) => {
    return await axios
      .post(
        `${API_BASE_URL}/academic-misconducts`,
        {
          date: academicMisconductDetails.date,
          class_code: academicMisconductDetails.class_code,
          reg_no: academicMisconductDetails.reg_no,
          outcome: academicMisconductDetails.outcome,
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

  getAcademicMisconductsForStudent: async (
    regNo: string,
    accessToken: string
  ) => {
    return await axios
      .get(`${API_BASE_URL}/academic-misconducts/${regNo}`, {
        data: { reg_no: regNo },
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when retrieving academic misconducts for the student.",
          error
        );
        throw error;
      });
  },
};
