import * as React from "react";

import { DocumentIcon, XMarkIcon } from "@heroicons/react/24/outline";

const MarksUploadedFile = ({
  file,
  setFile,
}: {
  file: File;
  setFile: (file: File | null) => void;
}) => {
  return (
    <div className="flex flex-row justify-between items-center mx-6 rounded-md border-2 border-dashed border-gray-300 p-4">
      <div className="flex flex-row space-x-4">
        <DocumentIcon className="h-8 w-8" />
        <div className="space-y-1">
          <h2 className="font-bold text-xs">{file.name}</h2>
          <h3 className="text-xs">{Math.round(file.size / 1024)}KB</h3>
        </div>
      </div>
      <XMarkIcon
        className="h-8 w-8 flex self-center hover:cursor-pointer"
        onClick={() => {
          setFile(null);
        }}
      />
    </div>
  );
};

export default MarksUploadedFile;
