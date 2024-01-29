import { IClassUploaded } from "./IClass";

export interface IUser {
  id: number;
  first_name: string;
  last_name: string;
}

export interface IUserLoginDetails {
  username: string;
  password: string;
}

export interface IUserDropdown {
  value: string;
  label: string;
}

export interface IUserDTO {
  email_address: string;
  first_name: string;
  last_name: string;
  access_token: string;
  refresh_token: string;
  roles: string[];
  classses: string[];
}

export interface ILecturer extends IUser {
  number_of_classes_taught: number;
  classes: IClassUploaded[];
}

export interface IUserEdit extends IUser {
  password: string | null;
  confirm_passsword: string | null;
}
