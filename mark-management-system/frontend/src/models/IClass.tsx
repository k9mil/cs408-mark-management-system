import { IAcademicMisconduct } from "./IAcademicMisconduct";
import { IStudent } from "./IStudent";
import { IUser } from "./IUser";

interface IBaseClass {
  name: string;
  code: string;
  credit: number;
  credit_level: number;
  lecturer_id: number | null;
}

export interface IClass extends IBaseClass {
  id: number;
  number_of_students: number;

  academic_misconduct: IAcademicMisconduct;
  lecturer: IUser;
  students: IStudent[];
}

export interface IClassWithLecturerId extends IBaseClass {
  lecturer_id: number | null;
}

export interface IClassWithId extends IClassWithLecturerId {
  id: number;
  original_code: string;
}

export interface IClassUploaded {
  name: string;
  code: string;
  credit: number;
  credit_level: number;
  is_uploaded: boolean;
}

export interface IClassBaseMetric extends IBaseClass {
  mean: number;
  stdev: number;
}
