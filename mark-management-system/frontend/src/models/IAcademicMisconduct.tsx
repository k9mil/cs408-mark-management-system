export interface IAcademicMisconduct {
  date: Date;
  class_code: number;
  reg_no: string;
  outcome: string;
}

export interface IAcademicMisconductRow {
  date: Date;
  module: number;
  module_name: string;
  reg_no: string;
  outcome: string;
}
