import { ReactNode } from "react";

export interface IAuthContext {
  isAuthenticated: boolean;
  updateAuthentication: (status: boolean) => void;
}

export interface IAuthProvider {
  children: ReactNode;
}
