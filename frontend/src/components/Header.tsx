import React from "react";
import { NavLink } from "react-router-dom";

const Header: React.FC = () => {
  return (
    <header className="bg-gray-700 text-white p-4">
      <NavLink to="/">
        <h1 className="text-2xl font-semibold">ESG Survey Automation</h1>
      </NavLink>
    </header>
  );
};

export default Header;
