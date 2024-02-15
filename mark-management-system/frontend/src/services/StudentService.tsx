import axios from "axios";

import { IStudentBase } from "../models/IStudent";

import { API_BASE_URL } from "../utils/Constants";

export const studentService = {
  createStudent: async (studentDetails: IStudentBase, accessToken: string) => {
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

  getStudent: async (regNo: string, accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/students/${regNo}`, {
        data: { reg_no: regNo },
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

  getStudents: async (accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/students/`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when retrieving all students.",
          error
        );
        throw error;
      });
  },
};
