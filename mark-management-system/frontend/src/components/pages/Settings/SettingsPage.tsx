import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "@/AuthProvider";

import { Button } from "@/components/common/Button";
import { Label } from "@/components/common/Label";
import { Input } from "@/components/common/Input";

import { Card, CardHeader, CardTitle } from "@/components/common/Card";

import Sidebar from "@/components/common/Sidebar";

import { IUserEdit } from "@/models/IUser";

import { userService } from "@/services/UserService";

import { toast } from "sonner";

import { validateUserEditDetails } from "@/utils/UserUtils";

const SettingsPage = () => {
  const navigate = useNavigate();
  const { id, firstName, lastName, isAuthenticated, getAccessToken } =
    useAuth();

  const accessToken = getAccessToken();

  useEffect(() => {
    document.title = "Mark Management System | Settings";

    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  const [formFirstName, setFirstName] = useState(firstName);
  const [formLastName, setLastName] = useState(lastName);
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const editUser = async (userDetails: IUserEdit) => {
    try {
      if (accessToken) {
        if (
          formFirstName !== firstName ||
          formLastName !== lastName ||
          password !== ""
        ) {
          await userService.editUser(userDetails, accessToken);
          toast.success("User was edited successfully!");
        } else {
          toast.info("Nothing was changed as no fields were edited.");
        }
      }
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when editing the user details.");
    }
  };

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center">
        <Card className="w-1/2 2xl:h-3/5 xl:h-4/5 space-y-2 p-6 flex flex-col">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle>Account Settings</CardTitle>
          </CardHeader>
          <div className="flex flex-row justify-between mx-6">
            <div className="space-y-4">
              <div>
                <Label htmlFor="firstName" className="text-right">
                  First Name
                </Label>
                <Input
                  id="firstName"
                  className="col-span-3"
                  value={formFirstName}
                  placeholder="John"
                  onChange={(e) => setFirstName(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="lastName" className="text-right">
                  Last Name
                </Label>
                <Input
                  id="lastName"
                  className="col-span-3"
                  value={formLastName}
                  placeholder="Doe"
                  onChange={(e) => setLastName(e.target.value)}
                />
              </div>
            </div>
          </div>
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle>Password Settings</CardTitle>
          </CardHeader>
          <div className="flex flex-row justify-between mx-6">
            <div className="space-y-4">
              <div>
                <Label htmlFor="password" className="text-right">
                  Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  className="col-span-3"
                  value={password}
                  placeholder="••••••••"
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <div>
                <Label htmlFor="confirmPassword" className="text-right">
                  Confirm Password
                </Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  className="col-span-3"
                  value={confirmPassword}
                  placeholder="••••••••"
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>
            </div>
          </div>
          <div className="flex self-end space-x-4">
            <Button
              className="flex self-end"
              variant="destructive"
              onClick={() => {
                setFirstName(firstName);
                setLastName(lastName);
                setPassword("");
                setConfirmPassword("");

                toast.info("Your fields have been reset.");
              }}
            >
              Reset
            </Button>
            <Button
              className="flex self-end"
              onClick={() => {
                const userDetails: IUserEdit = {
                  id: id,
                  first_name: formFirstName,
                  last_name: formLastName,
                  password: password,
                  confirm_passsword: confirmPassword,
                };

                if (validateUserEditDetails(userDetails)) {
                  editUser(userDetails);
                }
              }}
            >
              Save Changes
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default SettingsPage;
