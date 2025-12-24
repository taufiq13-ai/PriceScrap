import React, { useState } from "react";
import './TopNavBar.css';
import { FaSearch, FaFilter } from 'react-icons/fa';
import logo from '../../assets/logo192.png';

export default function TopNavBar() {
  const [showFilter, setShowFilter] = useState(false);
  const [priceRange, setPriceRange] = useState([0, 1000]); // [min, max]

  const toggleFilter = () => {
    setShowFilter(prev => !prev);
  };

  const handlePriceChange = (e, index) => {
    const value = Number(e.target.value);
    const newRange = [...priceRange];
    newRange[index] = value;
    setPriceRange(newRange);
  };

  return (
    <nav className="top-nav">
      <div className="nav-left">
        <div className="logo">PriceCheckert</div>

        <div className="search-container">
          <input type="text" placeholder="Search products..." />
          <button className="search-btn">
            <FaSearch />
          </button>
          <button className="filter-btn" onClick={toggleFilter}>
            <FaFilter />
          </button>

          {showFilter && (
            <div className="filter-popup">
              <h4>Price Range</h4>
              <div className="slider-container">
                <label>Min: RM {priceRange[0]}</label>
                <input
                  type="range"
                  min="0"
                  max="5000"
                  value={priceRange[0]}
                  onChange={(e) => handlePriceChange(e, 0)}
                />
                <label>Max: RM {priceRange[1]}</label>
                <input
                  type="range"
                  min="0"
                  max="5000"
                  value={priceRange[1]}
                  onChange={(e) => handlePriceChange(e, 1)}
                />
              </div>
              <button className="apply-btn" onClick={() => setShowFilter(false)}>Apply</button>
            </div>
          )}
        </div>
      </div>

      <div className="nav-right">
        <img src={logo} alt="Logo" className="logo-image" />
      </div>
    </nav>
  );
}
