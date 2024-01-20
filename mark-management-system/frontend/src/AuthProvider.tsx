import React, { createContext, useContext, useState } from "react";

import { IAuthContext, IAuthProvider } from "./models/IAuth";

const defaultAuthContext: IAuthContext = {
  isAuthenticated: false,
  updateAuthentication: () => {},
};

export const AuthContext = createContext<IAuthContext>(defaultAuthContext);
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: IAuthProvider) => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    const token = localStorage.getItem("user");
    return !!token;
  });

  const updateAuthentication = (status: boolean) => {
    setIsAuthenticated(status);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, updateAuthentication }}>
      {children}
    </AuthContext.Provider>
  );
};
