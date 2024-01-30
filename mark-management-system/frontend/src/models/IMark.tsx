export interface IMark {
  unique_code: string;
  mark: number;
  class_id: number;
  student_id: number;
}

export interface IMarkRow {
  CLASS_CODE: string;
  REG_NO: string;
  MARK: number;
  STUDENT_NAME: string;
  DEGREE_LEVEL: string;
  DEGREE_NAME: string;
  UNIQUE_CODE: string;
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
