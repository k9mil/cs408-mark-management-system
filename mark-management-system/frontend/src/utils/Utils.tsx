import { IMarkRow, IMarkMyPlace } from "@/models/IMark";

// https://stackoverflow.com/questions/23437476/in-typescript-how-to-check-if-a-string-is-numeric
export const isNumber = (value?: string | number): boolean => {
  return value != null && value !== "" && !isNaN(Number(value.toString()));
};

// https://stackoverflow.com/questions/12539574/whats-the-best-way-most-efficient-to-turn-all-the-keys-of-an-object-to-lower
export const toLowerCaseIMarkRow = (fileContents: IMarkRow[]): IMarkRow[] => {
  return fileContents.map(
    (obj: IMarkRow) =>
      Object.fromEntries(
        Object.entries(obj).map(([key, value]) => [key.toLowerCase(), value])
      ) as IMarkRow
  );
};

// https://stackoverflow.com/questions/12539574/whats-the-best-way-most-efficient-to-turn-all-the-keys-of-an-object-to-lower
export const toLowerCaseIMarkMyPlace = (
  fileContents: IMarkMyPlace[]
): IMarkMyPlace[] => {
  return fileContents.map(
    (obj: IMarkMyPlace) =>
      Object.fromEntries(
        Object.entries(obj).map(([key, value]) => [key.toLowerCase(), value])
      ) as IMarkMyPlace
  );
};

export const generateCSVname = (page: string): string => {
  const date = new Date();

  return `mms_${page}_${date.toISOString()}.csv`;
};
