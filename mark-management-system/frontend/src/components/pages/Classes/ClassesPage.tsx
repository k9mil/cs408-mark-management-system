import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../AuthProvider";

import Sidebar from "../../common/Sidebar";

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

import { classService } from "../../../services/ClassService";
import { userService } from "../../../services/UserService";

import { IClass, IClassWithLecturerId } from "../../../models/IClass";
import { IUser } from "../../../models/IUser";

import { validateClassDetails } from "../../../utils/ClassUtils";

import { toast } from "sonner";

import { PlusIcon } from "@heroicons/react/24/outline";

const ClassesPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/");
    }
  }, [navigate, isAuthenticated]);

  const [openDialogRow, setOpenDialogRow] = useState<boolean>(false);

  const [classes, setClasses] = useState<IClass[]>([]);
  const [lecturerOpen, setLecturerOpen] = React.useState(false);
  const [lecturer, setLecturer] = React.useState("");
  const [lecturers, setLecturers] = useState<IUser[]>([]);

  const [name, setName] = useState("");
  const [code, setCode] = useState("");
  const [credits, setCredits] = useState(0);
  const [creditLevel, setCreditLevel] = useState(0);

  const classData = async () => {
    try {
      const result = await classService.getClasses();
      setClasses(result);
    } catch (error) {
      console.error(error);
    }
  };

  const lecturerData = async () => {
    try {
      const result = await userService.getUsers();
      setLecturers(result);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    classData();
    lecturerData();
  }, []);

  const createClass = async (classDetails: IClassWithLecturerId) => {
    try {
      await classService.createClass(classDetails);
      toast.success("Class was created successfully!");

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
          <div className="flex flex-col space-y-4">
            <h1 className="text-3xl font-bold">Classes</h1>
            <div className="flex justify-between">
              <h2 className="text-gray-400">
                View a list of classes in the system
              </h2>
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
                      Enter then details of the new class. Click done when
                      you're finished.
                    </DialogDescription>
                  </DialogHeader>
                  <div className="flex flex-row justify-between">
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
                          lecturer_id: +lecturer,
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
            </div>
          </div>
          <ClassesDataTable
            columns={ClassColumns}
            data={classes}
            lecturers={lecturers}
            classData={classData}
            lecturerData={lecturerData}
          />
        </div>
      </div>
    </div>
  );
};

export default ClassesPage;
