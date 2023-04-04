import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import { useState, useEffect} from "react";

function Navbar() {
  const [navOpen, setNavOpen] = useState(false);

  const toggleNavOpen = () => {
    setNavOpen(!navOpen);
  }

  useEffect(() => {}, []);

  return (
    <nav className={navOpen ? "Navbar Navbar-open" : "Navbar"}>
        <span className="Navbar-title"><Link className="Nav-title-link" to="/home">📰 UK News Topic Modelling</Link></span>
        <ul className='Nav-links'>
            <li className='highlighted-link'><Link to='/intro'>Introduction</Link></li>
            <li className='highlighted-link'><Link to='/guardian'>The Guardian</Link></li>
            <li className='highlighted-link'><Link to='/mirror'>The Mirror</Link></li>
            <li className='highlighted-link'><Link to='/metro'>Metro</Link></li>
            <li className='highlighted-link'><Link to='/mail'>Daily Mail</Link></li>
            <li className='highlighted-link'><Link to='/telegraph'>Telegraph</Link></li>
            <li className='highlighted-link'><Link to='/sun'>Sun</Link></li>
            <li className='highlighted-link'><Link to='/express'>Express</Link></li>
        <button class={navOpen ? "burger burger-open" : "burger"} id="burger-toggle" onClick={()=>toggleNavOpen()}>
          <div id="open-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="black" fill="black" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <line x1="4" y1="6" x2="20" y2="6" />
            <line x1="4" y1="12" x2="20" y2="12" />
            <line x1="4" y1="18" x2="20" y2="18" />
            </svg>
          </div>
          <div id="close-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="44" height="44" viewBox="0 0 24 24" stroke-width="1.5" stroke="black" fill="black" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <rect x="4" y="4" width="16" height="16" rx="2" />
            <path d="M10 10l4 4m0 -4l-4 4" />
            </svg>
          </div>
        </button>
        </ul>
    </nav>
  )
}

export default Navbar