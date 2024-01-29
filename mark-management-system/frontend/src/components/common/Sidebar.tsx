import * as React from "react";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/common/Dialog";

import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

import { useAuth } from "../../AuthProvider";

import { userService } from "../../services/UserService";

import { toast } from "sonner";

import {
  HomeIcon,
  PencilIcon,
  UserGroupIcon,
  UserIcon,
  MagnifyingGlassCircleIcon,
  Cog8ToothIcon,
  InformationCircleIcon,
} from "@heroicons/react/24/outline";

import { Button } from "@/components/common/Button";

const Sidebar = () => {
  const navigate = useNavigate();
  const { isAdmin, updateAuthentication } = useAuth();

  const logout = async () => {
    try {
      await userService.logout();
      toast.success("You have successfully been logged out!");
      updateAuthentication(false);
      navigate("/");
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when logging out.");
    }
  };

  return (
    <>
      <nav className="h-screen w-1/6 bg-primary-blue flex flex-col justify-between border-r-2 border-black">
        <div>
          <div className="border-b-2 border-black">
            <img src="/strathclyde_logo.svg" alt="Strathclyde Logo" />
          </div>
          <ul>
            <li>
              <Link
                to="/dashboard"
                className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer"
              >
                <HomeIcon className="h-6 w-6 text-white" />
                <h2 className="text-white">Dashboard</h2>
              </Link>
            </li>
            <li>
              <Link
                to="/marks"
                className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer"
              >
                <PencilIcon className="h-6 w-6 text-white" />
                <h2 className="text-white">Marks</h2>
              </Link>
            </li>
            <li>
              <Link
                to="/classes"
                className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer"
              >
                <UserGroupIcon className="h-6 w-6 text-white" />
                <h2 className="text-white">Classes</h2>
              </Link>
            </li>
            <li>
              <Link
                to="/students"
                className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer"
              >
                <UserIcon className="h-6 w-6 text-white" />
                <h2 className="text-white">Students</h2>
              </Link>
            </li>
            <li>
              <Link
                to="/help"
                className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer"
              >
                <MagnifyingGlassCircleIcon className="h-6 w-6 text-white" />
                <h2 className="text-white">Help & Support</h2>
              </Link>
            </li>
            <li>
              <Link
                to="/settings"
                className="h-16 flex items-center space-x-4 hover:bg-hover-blue px-6 cursor-pointer"
              >
                <Cog8ToothIcon className="h-6 w-6 text-white" />
                <h2 className="text-white">Settings</h2>
              </Link>
            </li>
          </ul>
        </div>
        <div className="flex justify-between mx-6 my-4">
          <Dialog>
            <DialogTrigger asChild>
              <InformationCircleIcon className="h-6 w-6 text-white cursor-pointer" />
            </DialogTrigger>
            <DialogContent>
              <DialogHeader className="space-y-4">
                <DialogTitle className="text-xl">
                  Mark Management System
                </DialogTitle>
                <DialogDescription>
                  Welcome to the Mark Manament System Portal! On the system you
                  will be able to perform a wide range of tasks involving
                  student grades, marks & classes.
                </DialogDescription>
                {isAdmin === true ? (
                  <>
                    <DialogDescription>
                      As an administrator on the platform, you have elevated
                      permissions and are able to create classes, assign
                      lecturers to classes, amend class details or remove
                      classes in it's entirety.
                    </DialogDescription>
                    <DialogDescription>
                      If you are simultaneously an administrator and a lecturer,
                      you also have the permission to upload marks for students
                      that you teach, which you can then view on the Students
                      subpage. The marks that you have uploaded can be amended,
                      or deleted.
                    </DialogDescription>
                  </>
                ) : (
                  <>
                    <DialogDescription>
                      As a lecturer on the platform, you have permissions to
                      upload marks for students that you teach, which you can
                      then view on the Students subpage. The marks that you have
                      uploaded can be amended, or deleted.
                    </DialogDescription>
                    <DialogDescription>
                      You also have permissions to view the Classes tab, which
                      displays the classes that you are assigned as a lecturer
                      to, in which you can view the details of the classes
                      including information such as the Class Code and the
                      Number of Students.
                    </DialogDescription>
                  </>
                )}
              </DialogHeader>
              <DialogTrigger asChild>
                <DialogFooter>
                  <Button type="submit">Close</Button>
                </DialogFooter>
              </DialogTrigger>
            </DialogContent>
          </Dialog>
          <h2
            className="text-gray-400 cursor-pointer"
            onClick={() => {
              logout();
            }}
          >
            Log Out
          </h2>
        </div>
      </nav>
    </>
  );
};

export default Sidebar;
