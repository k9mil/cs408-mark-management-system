import { IDegree } from "./IDegree";

export interface IStudent {
  id: number;
  reg_no: string;
  student_name: string;
  personal_circumstances: number | null;
  degree_id: number;

  degree: IDegree;
}

export interface IStudentCreate {
  reg_no: string;
  student_name: string;
  personal_circumstances: number | null;
  degree_id: number;
}

export interface IStudentWithId extends IStudent {
  id: number;
}
