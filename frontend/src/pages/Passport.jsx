// Passport.js
import React, { useState } from 'react';
import axios from 'axios';
import FileDropZone from '../components/FileDrop';
import './Passport.css'; // Ensure correct path

const Passport = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileDrop = async (file) => {
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('image', file);
    formData.append('type', 'passport');

    try {
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (err) {
      console.error("Error uploading file", err);
      setError("Failed to upload and process the image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="passport">
      <h1>Passport Scanner</h1>
      <FileDropZone onDrop={handleFileDrop} />
      {loading && <p>Processing...</p>}
      {error && <p className="error">{error}</p>}
      {result && (
        <div className="result">
          <h3>Extracted Information</h3>
          {/* <p><strong>All:</strong> {result.all}</p> */}
          <p><strong>Name:</strong> {result.name}</p>
          <p><strong>Document Number:</strong> {result.document_number}</p>
          <p><strong>Expiration Date:</strong> {result.expiration_date}</p>
        </div>
      )}
    </div>
  );
};

export default Passport;
