import * as React from "react";

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
      <div className="h-screen w-1/6 bg-primary-blue flex flex-col justify-between border-r-[1px] border-black">
        <div className="space-y-8">
          <div className="border-b-[1px] border-black">
            <img src="/strathclyde_logo.svg" alt="Strathclyde Logo" />
          </div>
          <div className="space-y-12">
            <div className="ml-7 flex space-x-4">
              <HomeIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">Dashboard</h2>
            </div>
            <div className="ml-7 flex space-x-4">
              <PencilIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">Marks</h2>
            </div>
            <div className="ml-7 flex space-x-4">
              <UserGroupIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">Students</h2>
            </div>
            <div className="ml-7 flex space-x-4">
              <ClipboardDocumentListIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">Reports</h2>
            </div>
            <div className="ml-7 flex space-x-4">
              <UserIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">User Management</h2>
            </div>
            <div className="ml-7 flex space-x-4">
              <MagnifyingGlassCircleIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">Help & Support</h2>
            </div>
            <div className="ml-7 flex space-x-4">
              <Cog8ToothIcon className="h-6 w-6 text-white" />
              <h2 className="text-white">Settings</h2>
            </div>
          </div>
        </div>
        <div className="flex justify-between mx-6 my-4">
          <InformationCircleIcon className="h-6 w-6 text-white" />
          <h2 className="text-gray-400">Log Out</h2>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
