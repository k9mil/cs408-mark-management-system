export interface IMark {
  unique_code: string;
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
  unique_code: string;
}

export interface IMarkEdit {
  unique_code: string;
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
