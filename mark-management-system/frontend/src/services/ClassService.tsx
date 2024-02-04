import axios from "axios";

import { IClassWithLecturerId, IClassWithId } from "../models/IClass";

import { API_BASE_URL } from "../utils/Constants";

export const classService = {
  createClass: async (
    classDetails: IClassWithLecturerId,
    accessToken: string
  ) => {
    return await axios
      .post(
        `${API_BASE_URL}/classes`,
        {
          name: classDetails.name,
          code: classDetails.code,
          credit: classDetails.credit,
          credit_level: classDetails.credit_level,
          lecturer_id: classDetails.lecturer_id,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      )
      .catch((error) => {
        console.error(
          "Error: There has been an issue when creating a class.",
          error
        );
        throw error;
      });
  },

  getClasses: async (accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/classes`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when fetching classes.",
          error
        );
        throw error;
      });
  },

  getClassesForLecturer: async (accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/classes/lecturer`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when fetching classes for a lecturer.",
          error
        );
        throw error;
      });
  },

  editClass: async (classDetails: IClassWithId, accessToken: string) => {
    return await axios
      .put(
        `${API_BASE_URL}/classes/${classDetails.id}`,
        {
          id: classDetails.id,
          name: classDetails.name,
          code: classDetails.code,
          original_code: classDetails.original_code,
          credit: classDetails.credit,
          credit_level: classDetails.credit_level,
          lecturer_id: classDetails.lecturer_id,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      )
      .catch((error) => {
        console.error(
          "Error: There has been an issue when editing class details.",
          error
        );
        throw error;
      });
  },

  deleteClass: async (classId: number, accessToken: string) => {
    return await axios
      .delete(`${API_BASE_URL}/classes/${classId}`, {
        data: { class_id: classId },
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
      .catch((error) => {
        console.error(
          "Error: There has been an issue when deleting a class.",
          error
        );
        throw error;
      });
  },

  getClass: async (classCode: string, accessToken: string) => {
    return await axios
      .get(`${API_BASE_URL}/classes/${classCode}`, {
        data: { class_code: classCode },
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

  checkIfClassIsAssociatedWithADegree: async (
    classCode: string,
    degreeLevel: string,
    degreeName: string,
    accessToken: string
  ) => {
    return await axios
      .get(
        `${API_BASE_URL}/classes/${classCode}/degree/${degreeLevel}/${degreeName}`,
        {
          data: {
            class_code: classCode,
            degree_level: degreeLevel,
            degree_name: degreeName,
          },
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
};
