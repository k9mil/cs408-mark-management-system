import React, { createContext, useContext, useState } from "react";

import { IAuthContext, IAuthProvider } from "./models/IAuth";

const defaultAuthContext: IAuthContext = {
  isAuthenticated: false,
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

  const [localData, _] = useState(() => {
    const userData = localStorage.getItem("user");

    if (userData) {
      return JSON.parse(userData);
    }
  });

  const updateAuthentication = (status: boolean) => {
    setIsAuthenticated(status);
  };

  const getAccessToken = () => {
    return localData.access_token;
  };

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, updateAuthentication, getAccessToken }}
    >
      {children}
    </AuthContext.Provider>
  );
};
