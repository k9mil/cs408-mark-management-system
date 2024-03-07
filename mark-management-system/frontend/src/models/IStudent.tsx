import { IClass } from "./IClass";
import { IDegree } from "./IDegree";

export interface IStudent {
  id: number;
  reg_no: string;
  student_name: string;
  year: number;

  degree_id: number;

  classes: IClass[];
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
  max_mark: number;
  min_mark: number;
  pass_rate: number;
}
