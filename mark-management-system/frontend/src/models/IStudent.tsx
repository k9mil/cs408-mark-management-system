export interface IStudent {
  reg_no: string;
  student_name: string;
  personal_circumstances: number | null;
  degree_id: number;
}

export interface IStudentWithId extends IStudent {
  id: number;
}
