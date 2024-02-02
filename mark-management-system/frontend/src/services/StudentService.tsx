import axios from "axios";

import { IStudentCreate } from "../models/IStudent";

import { API_BASE_URL } from "../utils/Constants";

export const studentService = {
  createStudent: async (
    studentDetails: IStudentCreate,
    accessToken: string
  ) => {
    return await axios
      .post(
        `${API_BASE_URL}/students`,
        {
          reg_no: studentDetails.reg_no,
          student_name: studentDetails.student_name,
          personal_circumstances: studentDetails.personal_circumstances,
          degree_id: studentDetails.degree_id,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      )
      .catch((error) => {
        console.error(
          "Error: There has been an issue when creating a student.",
          error
        );
        throw error;
      });
  },

  getStudent: async (studentRegNo: string, accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/students/${studentRegNo}`, {
        data: { reg_no: studentRegNo },
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
