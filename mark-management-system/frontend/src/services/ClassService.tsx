import axios from "axios";

import { IClassWithLecturerId, IClassWithId } from "../models/IClass";

import { API_BASE_URL } from "../utils/Constants";

export const classService = {
  createClass: async (classDetails: IClassWithLecturerId) => {
    console.log(classDetails);
    return await axios
      .post(`${API_BASE_URL}/classes`, {
        name: classDetails.name,
        code: classDetails.code,
        credit: classDetails.credit,
        credit_level: classDetails.credit_level,
        lecturer_id: classDetails.lecturer_id,
      })
      .catch((error) => {
        console.error(
          "Error: There has been an issue when creating a class.",
          error
        );
        throw error;
      });
  },

  getClasses: async () => {
    return await axios
      .get(`${API_BASE_URL}/classes`)
      .then((response) => response.data)
      .catch((error) => {
        console.error(
          "Error: There has been an issue when fetching classes.",
          error
        );
        throw error;
      });
  },

  editClass: async (classDetails: IClassWithId) => {
    return await axios
      .post(`${API_BASE_URL}/classes/${classDetails.id}`, {
        id: classDetails.id,
        name: classDetails.name,
        code: classDetails.code,
        credit: classDetails.credit,
        credit_level: classDetails.credit_level,
        lecturer_id: classDetails.lecturer_id,
      })
      .catch((error) => {
        console.error(
          "Error: There has been an issue when editing class details.",
          error
        );
        throw error;
      });
  },

  deleteClass: async (classId: number) => {
    return await axios
      .delete(`${API_BASE_URL}/classes/${classId}`, {
        data: { class_id: classId },
      })
      .catch((error) => {
        console.error(
          "Error: There has been an issue when deleting a class.",
          error
        );
        throw error;
      });
  },
};
