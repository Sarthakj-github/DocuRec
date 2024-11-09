// src/MainContent.jsx
// import React, { useRef } from 'react';
import { Route, Routes } from 'react-router-dom';
import Passport from '../pages/Passport';
import DL from '../pages/DL';
import WC from '../pages/Welcome';
import './MainContent.css';

const MainContent = () => {
  return (
    <main>
      <Routes>
        <Route path="/" element={<WC />} />
        <Route path="/passport" element={<Passport />} />
        <Route path="/dl" element={<DL />} />
      </Routes>
    </main>
  );
};

export default MainContent;
