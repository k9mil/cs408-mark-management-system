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
