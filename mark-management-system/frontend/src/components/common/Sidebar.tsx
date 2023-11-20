import * as React from "react";

import { Link } from "react-router-dom";

import {
  HomeIcon,
  PencilIcon,
  UserGroupIcon,
  ClipboardDocumentListIcon,
  UserIcon,
  MagnifyingGlassCircleIcon,
  Cog8ToothIcon,
  InformationCircleIcon,
} from "@heroicons/react/24/outline";

const Sidebar = () => {
  return (
    <>
      <nav className="h-screen w-1/6 bg-primary-blue flex flex-col justify-between border-r-2 border-black">
        <div>
          <div className="border-b-2 border-black">
            <img src="/strathclyde_logo.svg" alt="Strathclyde Logo" />
          </div>
          <ul>
            <li className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer">
              <Link to="/" className="flex items-center space-x-4">
                <HomeIcon className="h-6 w-6 text-white" />
                <h2 className="text-white">Dashboard</h2>
              </Link>
            </li>
            <li className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer">
              <Link to="/marks" className="flex items-center space-x-4">
                <PencilIcon className="h-6 w-6 text-white" />
                <h2 className="text-white">Marks</h2>
              </Link>
            </li>
            <li className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer">
              <UserGroupIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">Students</h2>
            </li>
            <li className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer">
              <ClipboardDocumentListIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">Reports</h2>
            </li>
            <li className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer">
              <UserIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">User Management</h2>
            </li>
            <li className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer">
              <MagnifyingGlassCircleIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">Help & Support</h2>
            </li>
            <li className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer">
              <Cog8ToothIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">Settings</h2>
            </li>
          </ul>
        </div>
        <div className="flex justify-between mx-6 my-4">
          <InformationCircleIcon className="h-6 w-6 text-white cursor-pointer" />
          <h2 className="text-gray-400 cursor-pointer">Log Out</h2>
        </div>
      </nav>
    </>
  );
};

export default Sidebar;
