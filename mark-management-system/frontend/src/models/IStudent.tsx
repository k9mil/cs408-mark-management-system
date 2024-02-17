import { IDegree } from "./IDegree";

export interface IStudent {
  id: number;
  reg_no: string;
  student_name: string;
  degree_id: number;

  degree: IDegree;
}

export interface IStudentBase {
  reg_no: string;
  student_name: string;
  degree_id: number;
}

export interface IStudentWithId extends IStudent {
  id: number;
}

export interface IStudentDetailsWithStatistics {
  mean: number;
  mode: number;
  median: number;
  pass_rate: number;
}
