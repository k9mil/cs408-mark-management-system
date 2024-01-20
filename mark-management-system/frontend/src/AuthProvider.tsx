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
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    const token = localStorage.getItem("user");
    return !!token;
  });

  const [localData, setLocalData] = useState(() => {
    const userData = localStorage.getItem("user");

    if (userData) {
      return JSON.parse(userData);
    }
  });

  const [isAdmin, setIsAdmin] = useState(() => {
    const userData = localStorage.getItem("user");

    if (userData) {
      const parsedUserData = JSON.parse(userData);
      const rolesAsAnArray: IRole[] = Object.values(parsedUserData.roles);

      console.log(userData);

      return rolesAsAnArray.some((role) => role.title === "admin");
    }
  });

  const updateAuthentication = (status: boolean) => {
    setIsAuthenticated(status);
  };

  const getAccessToken = () => {
    try {
      if (localData.access_token && isAuthenticated)
        return localData.access_token;
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
