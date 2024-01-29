import React, { useEffect } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import { Button } from "@/components/common/Button";
import { Label } from "@/components/common/Label";
import { Input } from "@/components/common/Input";

import { Card, CardHeader, CardTitle } from "@/components/common/Card";

import Sidebar from "../../common/Sidebar";

const SettingsPage = () => {
  const navigate = useNavigate();
  const { firstName, lastName, isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl flex justify-center items-center">
        <Card className="w-1/2 h-3/5 space-y-2 p-6 flex flex-col">
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
                  defaultValue={firstName}
                  placeholder="John"
                />
              </div>
              <div>
                <Label htmlFor="lastName" className="text-right">
                  Last Name
                </Label>
                <Input
                  id="lastName"
                  className="col-span-3"
                  defaultValue={lastName}
                  placeholder="Doe"
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
                  placeholder="••••••••"
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
                  placeholder="••••••••"
                />
              </div>
            </div>
          </div>
          <Button className="w-20 flex self-end" onClick={() => {}}>
            Next
          </Button>
        </Card>
      </div>
    </div>
  );
};

export default SettingsPage;
