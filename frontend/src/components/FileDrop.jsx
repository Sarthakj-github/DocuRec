// FileDropZone.js
import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { AiOutlineCloudUpload } from 'react-icons/ai';
import './FileDrop.css'; // Ensure you have this CSS file

const FileDropZone = ({ onDrop }) => {
  const handleDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onDrop(acceptedFiles[0]); // Pass the file back to the parent component
    }
  }, [onDrop]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: handleDrop,
    accept: 'image/*'
  });

  return (
    <div {...getRootProps()} className="dropzone">
      <input {...getInputProps()} />
      <AiOutlineCloudUpload className="dropzone-icon" />
      {isDragActive ? (
        <p>Drop the image here...</p>
      ) : (
        <p>Drag & drop an image here, or click to select one</p>
      )}
    </div>
  );
};

export default FileDropZone;
