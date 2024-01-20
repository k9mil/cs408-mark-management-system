import * as React from "react";

import { Label } from "@/components/common/Label";
import { Input } from "@/components/common/Input";
import { Button } from "@/components/common/Button";

const LoginPage = () => {
  return (
    <div className="flex flex-row h-screen w-screen">
      <div className="w-1/2 bg-primary-blue flex flex-col justify-between">
        <div className="">
          <img src="/strathclyde_logo.svg" alt="Strathclyde Logo" />
        </div>
        <h2 className="text-xl text-white font-semibold m-8">
          “The place of useful learning.”
        </h2>
      </div>
      <div className="w-1/2 flex justify-center items-center">
        <div className="flex flex-col space-y-12">
          <div className="flex flex-col items-center space-y-2">
            <h1 className="font-semibold text-xl">
              Welcome Back! Please Log In
            </h1>
            <h2 className="text-gray-400 text-sm font-light">
              Enter your details below to access your account.
            </h2>
          </div>
          <div className="flex flex-col space-y-4">
            <div>
              <Label htmlFor="email">Email</Label>
              <Input id="email" placeholder="name@example.com" type="email" />
            </div>
            <div>
              <Label htmlFor="password">Password</Label>
              <Input id="password" placeholder="•••••••••" type="password" />
            </div>
            <Button>Sign In with Email</Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
