export interface IMark {
  mark: number;
  class_id: number;
  student_id: number;
}

export interface IMarkRow {
  id: number;
  class_code: string;
  reg_no: string;
  mark: number;
  student_name: string;
  degree_level: string;
  degree_name: string;
}

export interface IMarkMMS {
  class_code: string;
  reg_no: string;
  mark: number;
  student_name: string;
  degree_level: string;
  degree_name: string;
}

export interface IMarkPegasus {
  class_code: string;
  reg_no: string;
  mark: number;
  mark_code: string;
  student_name: string;
  course: string;
  degree: string;
  degree_code: string;
  result: string;
}

export interface IMarkEdit {
  id: number;
  mark: number | null;
}

export interface IStatistics {
  mean: number;
  median: number;
  mode: number;
  pass_rate: number;
}

export interface IMarkMyPlace {
  class_code: string;
  date: Date;
  reg_no: string;
  class_total: number;
  override_mark: number;
}
