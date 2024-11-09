// src/components/Header.js
import React from 'react';
import NavLink from './NavLink';
import './Header.css';  // Import the CSS file

const Header = () => {
  return (
    <header>
      <nav>
        <ul>
          <NavLink to="/" label="Home" />
          <NavLink to="/passport" label="Passport" />
          <NavLink to="/dl" label="DL" />
        </ul>
      </nav>
    </header>
  );
};

export default Header;
