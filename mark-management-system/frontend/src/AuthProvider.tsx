import React, { createContext, useContext, useState } from "react";

import { IAuthContext, IAuthProvider } from "./models/IAuth";
import { IRole } from "./models/IRole";

const defaultAuthContext: IAuthContext = {
  id: 0,
  isAuthenticated: false,
  isAdmin: false,
  isLecturer: false,
  firstName: "",
  lastName: "",
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

  const isLecturerCheck = (): boolean => {
    if (localData) {
      const rolesAsAnArray: IRole[] = Object.values(localData.roles);

      return rolesAsAnArray.some((role) => role.title === "lecturer");
    }

    return false;
  };

  const [isAdmin, setIsAdmin] = useState<boolean>(isAdminCheck());
  const [isLecturer, setIsLecturer] = useState<boolean>(isLecturerCheck());

  const updateAuthentication = (status: boolean) => {
    setIsAuthenticated(status);

    const userData = localStorage.getItem("user");

    if (userData) {
      const parsedUserData = JSON.parse(userData);
      setLocalData(parsedUserData);

      const rolesAsAnArray: IRole[] = Object.values(parsedUserData.roles);

      setIsAdmin(rolesAsAnArray.some((role) => role.title === "admin"));
      setIsLecturer(rolesAsAnArray.some((role) => role.title === "lecturer"));
    }
  };

  const retrieveFirstName = () => {
    if (localData) {
      return localData.first_name;
    }

    return "";
  };

  const retrieveLastName = () => {
    if (localData) {
      return localData.last_name;
    }

    return "";
  };

  const [firstName] = useState(retrieveFirstName());
  const [lastName] = useState(retrieveLastName());

  const retrieveId = () => {
    if (localData) {
      return localData.id;
    }

    return 0;
  };

  const [id] = useState(retrieveId());

  const getAccessToken = () => {
    try {
      if (localData && isAuthenticated) return localData.access_token;
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        id,
        isAuthenticated,
        isAdmin,
        isLecturer,
        firstName,
        lastName,
        updateAuthentication,
        getAccessToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
