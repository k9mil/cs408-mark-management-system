import * as React from "react";

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
        <div className="flex flex-col">
          <div className="flex flex-col items-center space-y-4">
            <h1 className="font-bold text-2xl">Welcome Back! Please Log In</h1>
            <h2 className="text-gray-400">
              Enter your email and password below to access your account
            </h2>
          </div>
          <div></div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
