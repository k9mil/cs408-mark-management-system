import { IUser } from "./IUser";

interface IBaseClass {
  name: string;
  code: string;
  credit: number;
  credit_level: number;
  lecturer_id: number;
}

export interface IClass extends IBaseClass {
  number_of_students: number;
  lecturer: IUser;
}

export interface IClassWithLecturerId extends IBaseClass {
  lecturer_id: number;
}

export interface IClassWithId extends IClassWithLecturerId {
  id: number;
  original_code: number;
}
