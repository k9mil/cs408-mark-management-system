import React, { createContext, useContext, useState } from "react";

import { IAuthContext, IAuthProvider } from "./models/IAuth";
import { IRole } from "./models/IRole";

const defaultAuthContext: IAuthContext = {
  isAuthenticated: false,
  isAdmin: false,
  updateAuthentication: () => {},
  getAccessToken: () => null,
};

export const AuthContext = createContext<IAuthContext>(defaultAuthContext);
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: IAuthProvider) => {
  const retrieveLocalData = () => {
    const userDataString = localStorage.getItem("user");
    return userDataString ? JSON.parse(userDataString) : null;
  };

  const [localData, setLocalData] = useState(retrieveLocalData());
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(!!localData);

  const isAdminCheck = (): boolean => {
    if (localData) {
      const rolesAsAnArray: IRole[] = Object.values(localData.roles);

      return rolesAsAnArray.some((role) => role.title === "admin");
    }

    return false;
  };

  const [isAdmin, setIsAdmin] = useState<boolean>(isAdminCheck());

  const updateAuthentication = (status: boolean) => {
    setIsAuthenticated(status);

    const userData = localStorage.getItem("user");

    if (userData) {
      const parsedUserData = JSON.parse(userData);
      setLocalData(parsedUserData);

      const rolesAsAnArray: IRole[] = Object.values(parsedUserData.roles);
      setIsAdmin(rolesAsAnArray.some((role) => role.title === "admin"));
    }
  };

  const getAccessToken = () => {
    try {
      if (localData && isAuthenticated) return localData.access_token;
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, isAdmin, updateAuthentication, getAccessToken }}
    >
      {children}
    </AuthContext.Provider>
  );
};
