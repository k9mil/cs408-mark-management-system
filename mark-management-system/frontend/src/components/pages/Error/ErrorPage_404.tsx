import React, { useEffect } from "react";

import { Button } from "@/components/common/Button";

import { useNavigate } from "react-router-dom";

const ErrorPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    document.title = "Mark Management System | 404";
  }, []);

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
      <div className="w-1/2 flex flex-col justify-center items-center">
        <div className="flex flex-col -space-y-12 justify-center items-center">
          <div className="w-96 h-96">
            <img src="/404_error.svg" alt="404 Error Illustration" />
          </div>
          <div className="flex flex-col space-y-8">
            <h1 className="flex self-center font-bold text-3xl">
              Oops, something went wrong.
            </h1>
            <Button
              className="w-1/2 flex self-center"
              onClick={() => {
                navigate("/");
              }}
            >
              Go to Homepage
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ErrorPage;
