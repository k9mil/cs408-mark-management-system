import { ReactNode } from "react";

export interface IAuthContext {
  isAuthenticated: boolean;
  isAdmin: boolean;
  updateAuthentication: (status: boolean) => void;
  getAccessToken: () => string | null;
}

export interface IAuthProvider {
  children: ReactNode;
}
