import { IMarkRow } from "@/models/IMark";

// https://stackoverflow.com/questions/23437476/in-typescript-how-to-check-if-a-string-is-numeric
export function isNumber(value?: string | number): boolean {
  return value != null && value !== "" && !isNaN(Number(value.toString()));
}

// https://stackoverflow.com/questions/12539574/whats-the-best-way-most-efficient-to-turn-all-the-keys-of-an-object-to-lower
export function toLowerCase(fileContents: IMarkRow[]) {
  return fileContents.map((obj: IMarkRow) =>
    Object.fromEntries(
      Object.entries(obj).map(([key, value]) => [key.toLowerCase(), value])
    )
  );
}
