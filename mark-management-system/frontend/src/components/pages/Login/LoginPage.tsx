import React, { useState } from "react";

import { useNavigate } from "react-router-dom";

import { Label } from "@/components/common/Label";
import { Input } from "@/components/common/Input";
import { Button } from "@/components/common/Button";
import { Spinner } from "@/components/common/Spinner";

import { userService } from "../../../services/UserService";

import { IUserLoginDetails } from "../../../models/IUser";

import { toast } from "sonner";

const LoginPage = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = React.useState<boolean>(false);

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const userDetails: IUserLoginDetails = {
      username: email,
      password: password,
    };

    await authenticateUser(userDetails);
  };

  const authenticateUser = async (userDetails: IUserLoginDetails) => {
    setIsLoading(true);

    try {
      await userService.authenticateUser(userDetails);
      toast.success("You have successfully been authenticated!");
      navigate("/dashboard");
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when logging in.");
    } finally {
      setIsLoading(false);
    }
  };

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
            <h1 className="font-bold text-2xl">Welcome Back! Please Log In</h1>
            <h2 className="text-gray-400 text-sm font-light">
              Enter your details below to access your account.
            </h2>
          </div>
          <form className="flex flex-col space-y-4" onSubmit={onSubmit}>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                placeholder="name@example.com"
                type="email"
                onChange={(e) => setEmail(e.target.value)}
                disabled={isLoading}
              />
            </div>
            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                placeholder="•••••••••"
                type="password"
                onChange={(e) => setPassword(e.target.value)}
                disabled={isLoading}
              />
            </div>
            <Button>
              {isLoading && <Spinner />}
              Sign In with Email
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
