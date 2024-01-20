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
