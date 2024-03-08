export interface IDegree {
  name: string;
  level: string;
  code: string;
}

export interface IDegreeWithId extends IDegree {
  id: number;
}
