import React, { createContext, useContext, useState, useRef } from "react";

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
  const isAdmin = useRef(false);

  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    const token = localStorage.getItem("user");
    return !!token;
  });

  const [localData, setLocalData] = useState();

  const updateAuthentication = (status: boolean) => {
    setIsAuthenticated(status);

    const userData = localStorage.getItem("user");

    if (userData) {
      const parsedUserData = JSON.parse(userData);
      setLocalData(parsedUserData);

      const rolesAsAnArray: IRole[] = Object.values(parsedUserData.roles);
      isAdmin.current = rolesAsAnArray.some((role) => role.title === "admin");
    }
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
