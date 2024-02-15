import axios from "axios";

import { IMark, IMarkEdit } from "../models/IMark";

import { API_BASE_URL } from "../utils/Constants";

export const markService = {
  createMark: async (markDetails: IMark, accessToken: string) => {
    return await axios
      .post(
        `${API_BASE_URL}/marks`,
        {
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

  getMark: async (studentId: number, classId: number, accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/marks/${studentId}/${classId}`, {
        data: { stuent_id: studentId, class_id: classId },
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

  getStudentMarks: async (accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/marks`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when retrieving student marks.",
          error
        );
        throw error;
      });
  },

  getStatistics: async (accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/marks/statistics/`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when retrieving student statistics.",
          error
        );
        throw error;
      });
  },

  editMark: async (markDetails: IMarkEdit, accessToken: string) => {
    return await axios
      .put(
        `${API_BASE_URL}/marks/${markDetails.id}`,
        {
          id: markDetails.id,
          mark: markDetails.mark,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      )
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when retrieving student statistics.",
          error
        );
        throw error;
      });
  },

  deleteMark: async (markId: number, accessToken: string) => {
    return await axios
      .delete(`${API_BASE_URL}/marks/${markId}`, {
        data: { mark_id: markId },
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when retrieving student statistics.",
          error
        );
        throw error;
      });
  },

  getMarksForStudent: async (regNo: string, accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/marks/${regNo}/all/`, {
        data: { regNo: regNo },
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when retrieving marks for the student.",
          error
        );
        throw error;
      });
  },
};
