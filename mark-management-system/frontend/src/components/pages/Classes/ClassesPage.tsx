import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "@/AuthProvider";

import Sidebar from "@/components/common/Sidebar";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/common/Dialog";

import { Label } from "@/components/common/Label";
import { Input } from "@/components/common/Input";
import { Button } from "@/components/common/Button";

import { ClassesLecturerDropdown } from "./ClassesLecturerDropdown";

import { ClassesDataTable } from "./ClassesDataTable";
import { ClassColumns } from "./ClassesColumns";

import { classService } from "@/services/ClassService";
import { userService } from "@/services/UserService";

import { IClass, IClassWithLecturerId } from "@/models/IClass";
import { IUser } from "@/models/IUser";

import { validateClassDetails } from "@/utils/ClassUtils";

import { toast } from "sonner";

import { PlusIcon } from "@heroicons/react/24/outline";

const ClassesPage = () => {
  const navigate = useNavigate();
  const { isAdmin, isLecturer, isAuthenticated, getAccessToken } = useAuth();

  useEffect(() => {
    if (!isAuthenticated || (!isAdmin && !isLecturer)) {
      navigate("/");
    }
  }, [navigate, isAuthenticated, isAdmin, isLecturer]);

  const [openDialogRow, setOpenDialogRow] = useState<boolean>(false);

  const [classes, setClasses] = useState<IClass[]>([]);
  const [lecturerOpen, setLecturerOpen] = React.useState<boolean>(false);
  const [lecturer, setLecturer] = React.useState<string>("");
  const [lecturers, setLecturers] = useState<IUser[]>([]);

  const [name, setName] = useState<string>("");
  const [code, setCode] = useState<string>("");
  const [credits, setCredits] = useState<number>(0);
  const [creditLevel, setCreditLevel] = useState<number>(0);

  const accessToken = getAccessToken();

  const classData = async () => {
    try {
      if (accessToken) {
        if (isAdmin) {
          const result = await classService.getClasses(accessToken);
          setClasses(result);
        } else {
          const result = await classService.getClassesForLecturer(accessToken);
          setClasses(result);
        }
      }
    } catch (error) {
      console.error(error);
    }
  };

  const lecturerData = async () => {
    try {
      if (accessToken) {
        if (isAdmin) {
          const result = await userService.getLecturers(accessToken);
          setLecturers(result);
        }
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    document.title = "Mark Management System | Classes";

    classData();
    lecturerData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const createClass = async (classDetails: IClassWithLecturerId) => {
    try {
      if (accessToken) {
        await classService.createClass(classDetails, accessToken);
        toast.success("Class was created successfully!");
      }

      classData();
      setOpenDialogRow(false);
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong when creating the class.");
    }
  };

  const lecturerList = lecturers.map((user) => ({
    value: user.id.toString(),
    label: `${user.first_name} ${user.last_name}`,
  }));

  return (
    <div className="bg-primary-blue h-screen w-screen flex">
      <Sidebar />
      <div className="w-4/5 h-[95vh] m-auto bg-slate-100 rounded-3xl">
        <div className="m-8 flex flex-col space-y-4">
          <div className="flex 2xl:flex-col xl:flex-row 2xl:space-y-1 xl:space-x-2 2xl:space-x-0 xl:items-center 2xl:items-start">
            <h1 className="text-3xl font-bold">Classes</h1>
            <div className="flex justify-between xl:w-full">
              <h2 className="text-gray-600">
                View a list of classes or a create a new class in the system
              </h2>
              {isAdmin === true ? (
                <Dialog
                  open={openDialogRow === true}
                  onOpenChange={(open) => {
                    if (!open) setOpenDialogRow(false);
                  }}
                >
                  <DialogTrigger asChild>
                    <PlusIcon
                      className="h-6 w-6 text-black cursor-pointer"
                      onClick={() => {
                        setOpenDialogRow(true);
                      }}
                    />
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader className="space-y-4">
                      <DialogTitle className="text-xl">
                        Create a Class
                      </DialogTitle>
                      <DialogDescription>
                        Enter the details of the new class. Click done when
                        you're finished.
                      </DialogDescription>
                    </DialogHeader>
                    <div className="flex flex-row justify-between gap-14">
                      <div className="space-y-4">
                        <div>
                          <Label htmlFor="name" className="text-right">
                            Name
                          </Label>
                          <Input
                            id="name"
                            className="col-span-3"
                            onChange={(e) => setName(e.target.value)}
                          />
                        </div>
                        <div>
                          <Label htmlFor="code" className="text-right">
                            Code
                          </Label>
                          <Input
                            id="code"
                            className="col-span-3"
                            onChange={(e) => setCode(e.target.value)}
                          />
                        </div>
                        <div>
                          <Label htmlFor="credits" className="text-right">
                            Credits
                          </Label>
                          <Input
                            id="credits"
                            className="col-span-3"
                            onChange={(e) => setCredits(+e.target.value)}
                          />
                        </div>
                      </div>
                      <div className="space-y-4">
                        <div>
                          <Label htmlFor="creditLevel" className="text-right">
                            Credit Level
                          </Label>
                          <Input
                            id="creditLevel"
                            className="col-span-3"
                            onChange={(e) => setCreditLevel(+e.target.value)}
                          />
                        </div>
                        <ClassesLecturerDropdown
                          lecturer={lecturer}
                          lecturerOpen={lecturerOpen}
                          setLecturer={setLecturer}
                          setLecturerOpen={setLecturerOpen}
                          lecturerList={lecturerList}
                        />
                      </div>
                    </div>
                    <DialogFooter>
                      <Button
                        type="submit"
                        onClick={() => {
                          const classDetails: IClassWithLecturerId = {
                            name: name,
                            code: code,
                            credit: +credits,
                            credit_level: +creditLevel,
                            lecturer_id: lecturer === "" ? null : +lecturer,
                          };

                          if (validateClassDetails(classDetails)) {
                            createClass(classDetails);
                          }
                        }}
                      >
                        Done
                      </Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              ) : null}
            </div>
          </div>
          <ClassesDataTable
            columns={ClassColumns}
            data={classes}
            lecturers={lecturers}
            classData={classData}
            lecturerData={lecturerData}
            accessToken={accessToken}
          />
        </div>
      </div>
    </div>
  );
};

export default ClassesPage;
