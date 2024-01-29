import { ReactNode } from "react";

export interface IAuthContext {
  isAuthenticated: boolean;
  isAdmin: boolean;
  isLecturer: boolean;
  firstName: string;
  lastName: string;
  updateAuthentication: (status: boolean) => void;
  getAccessToken: () => string | null;
}

export interface IAuthProvider {
  children: ReactNode;
}
